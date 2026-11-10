import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def conectar():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        raise ConnectionError(f"Falha ao conectar no MySQL: {e}")

# --- AUTENTICAÇÃO ---
def buscar_usuario(usuario: str, senha: str):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT id, usuario FROM usuarios WHERE usuario = %s AND senha = %s", (usuario, senha))
        return cursor.fetchone()
    finally:
        if cursor: cursor.close()
        if conexao and conexao.is_connected(): conexao.close()

def cadastrar_usuario(usuario: str, senha: str):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)", (usuario, senha))
        conexao.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        if cursor: cursor.close()
        if conexao and conexao.is_connected(): conexao.close()

# --- CLIENTES ---
def cadastrar_cliente(nome, cpf, telefone, endereco, cidade, obs, data):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "INSERT INTO clientes (nome, cpf, telefone, endereco, cidade, observacao, data_cadastro) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (nome, cpf, telefone, endereco, cidade, obs, data))
    conexao.commit()
    cursor.close()
    conexao.close()

def buscar_clientes(filtro=""):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = "SELECT * FROM clientes"
    params = []
    if filtro:
        sql += " WHERE nome LIKE %s"
        params.append(f"%{filtro}%")
    sql += " ORDER BY nome ASC"
    cursor.execute(sql, params)
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultado

# --- PRODUTOS ---
def cadastrar_produto(nome, marca, custo, venda, estoque, obs):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "INSERT INTO produtos (nome, marca, preco_custo, preco_venda, estoque, observacao) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (nome, marca, custo, venda, estoque, obs))
    conexao.commit()
    cursor.close()
    conexao.close()

def buscar_produtos(filtro=""):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = "SELECT * FROM produtos"
    params = []
    if filtro:
        sql += " WHERE nome LIKE %s"
        params.append(f"%{filtro}%")
    sql += " ORDER BY nome ASC"
    cursor.execute(sql, params)
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultado

# --- DASHBOARD (INÍCIO) ---
def obter_dados_dashboard():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    dados = {}
    
    # Vendas do mês e Lucro
    cursor.execute("""
        SELECT SUM(valor_final) as total_vendas, 
               SUM((iv.valor_unitario - p.preco_custo) * iv.quantidade) as lucro_total
        FROM vendas v
        JOIN itens_venda iv ON v.id = iv.venda_id
        JOIN produtos p ON iv.produto_id = p.id
        WHERE MONTH(v.data_venda) = MONTH(CURRENT_DATE()) AND YEAR(v.data_venda) = YEAR(CURRENT_DATE())
    """)
    res_vendas = cursor.fetchone()
    dados['vendas_mes'] = res_vendas['total_vendas'] if res_vendas['total_vendas'] else 0.0
    dados['lucro_mes'] = res_vendas['lucro_total'] if res_vendas['lucro_total'] else 0.0

    # A receber (Pendentes)
    cursor.execute("SELECT SUM(valor_final) as a_receber FROM vendas WHERE status = 'Pendente'")
    res_receber = cursor.fetchone()
    dados['a_receber'] = res_receber['a_receber'] if res_receber['a_receber'] else 0.0

    # Estoque total e baixo estoque
    cursor.execute("SELECT SUM(estoque) as total_estoque, COUNT(CASE WHEN estoque < 5 THEN 1 END) as baixo_estoque FROM produtos")
    res_estoque = cursor.fetchone()
    dados['total_estoque'] = res_estoque['total_estoque'] if res_estoque['total_estoque'] else 0
    dados['baixo_estoque'] = res_estoque['baixo_estoque'] if res_estoque['baixo_estoque'] else 0

    # Contas Pendentes (últimas 3)
    cursor.execute("""
        SELECT c.nome, v.valor_final, DATEDIFF(CURRENT_DATE(), v.data_venda) as dias_passados
        FROM vendas v JOIN clientes c ON v.cliente_id = c.id
        WHERE v.status = 'Pendente' ORDER BY v.data_venda ASC LIMIT 3
    """)
    dados['contas_pendentes'] = cursor.fetchall()

    # Vendas Recentes (últimas 3)
    cursor.execute("""
        SELECT c.nome as cliente, p.nome as produto, v.valor_final
        FROM vendas v 
        JOIN clientes c ON v.cliente_id = c.id
        JOIN itens_venda iv ON v.id = iv.venda_id
        JOIN produtos p ON iv.produto_id = p.id
        ORDER BY v.id DESC LIMIT 3
    """)
    dados['vendas_recentes'] = cursor.fetchall()

    cursor.close()
    conexao.close()
    return dados

# --- VENDAS E CONTAS ---
def registrar_venda(cliente_id, itens, desconto, forma_pgto, parcelas, status):
    conexao = conectar()
    cursor = conexao.cursor()
    
    total_bruto = sum(item['preco'] * item['qtd'] for item in itens)
    valor_final = total_bruto - desconto
    
    # 1. Insere a venda
    sql_venda = """INSERT INTO vendas (cliente_id, data_venda, valor_total, desconto, valor_final, forma_pagamento, parcelas, status) 
                   VALUES (%s, CURRENT_DATE(), %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql_venda, (cliente_id, total_bruto, desconto, valor_final, forma_pgto, parcelas, status))
    venda_id = cursor.lastrowid
    
    # 2. Insere os itens e baixa o estoque
    for item in itens:
        sql_item = "INSERT INTO itens_venda (venda_id, produto_id, quantidade, valor_unitario) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_item, (venda_id, item['id'], item['qtd'], item['preco']))
        
        sql_estoque = "UPDATE produtos SET estoque = estoque - %s WHERE id = %s"
        cursor.execute(sql_estoque, (item['qtd'], item['id']))
        
    conexao.commit()
    cursor.close()
    conexao.close()

def buscar_contas():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """SELECT v.id, c.nome as cliente, v.valor_final as valor, v.data_venda, v.status 
             FROM vendas v JOIN clientes c ON v.cliente_id = c.id ORDER BY v.data_venda DESC"""
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultado

def alterar_status_venda(venda_id, novo_status):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE vendas SET status = %s WHERE id = %s", (novo_status, venda_id))
    conexao.commit()
    cursor.close()
    conexao.close()