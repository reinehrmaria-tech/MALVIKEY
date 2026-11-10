import tkinter as tk
from database import obter_dados_dashboard
from telas.menu_lateral import MenuLateral

BG_APP        = "#F7F9FC"
COR_TEXTO     = "#2D3748"
COR_SUAVE     = "#A0AEC0"
COR_PRIMARIA  = "#6C4EE3"
COR_PENDENTE  = "#FED7D7"
COR_TXT_PEND  = "#E53E3E"

class TelaInicial:
    def __init__(self, root, dados_usuario):
        self.root = root
        self.root.title("Essência Rústica - Início")
        self.root.geometry("1200x750")
        self.root.configure(bg=BG_APP)
        self.root.state('zoomed')

        self.nome_usuario = dados_usuario['usuario']
        self.dados = obter_dados_dashboard()

        self._montar_tela()

    def _montar_tela(self):
        for w in self.root.winfo_children():
            w.destroy()

        # Menu Lateral
        MenuLateral(self.root, "inicio")

        # Área Principal
        main_frame = tk.Frame(self.root, bg=BG_APP)
        main_frame.pack(side="right", fill="both", expand=True)

        header = tk.Frame(main_frame, bg="white", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Início", font=("Segoe UI", 12, "bold"), bg="white", fg=COR_TEXTO).pack(side="left", padx=30)
        tk.Label(header, text=f"👤 {self.nome_usuario}", font=("Segoe UI", 10, "bold"), bg="white", fg=COR_TEXTO).pack(side="right", padx=20)

        corpo = tk.Frame(main_frame, bg=BG_APP, padx=30, pady=20)
        corpo.pack(fill="both", expand=True)

        tk.Label(corpo, text="ESSÊNCIA RÚSTICA", font=("Segoe UI", 9, "bold"), bg=BG_APP, fg=COR_PRIMARIA).pack(anchor="w")
        tk.Label(corpo, text="Olá!", font=("Segoe UI", 24, "bold"), bg=BG_APP, fg=COR_TEXTO).pack(anchor="w")
        tk.Label(corpo, text="Bem-vinda a Essência Rústica. Aqui está o resumo do seu negócio.", font=("Segoe UI", 10), bg=BG_APP, fg=COR_SUAVE).pack(anchor="w", pady=(0, 20))

        # Grid de Cards
        grid_cards = tk.Frame(corpo, bg=BG_APP)
        grid_cards.pack(fill="x", pady=10)

        def criar_card(parent, titulo, valor, subtexto, icon, cor_icon):
            card = tk.Frame(parent, bg="white", padx=20, pady=15, highlightbackground="#E2E8F0", highlightthickness=1)
            tk.Label(card, text=titulo, font=("Segoe UI", 8, "bold"), bg="white", fg=COR_SUAVE).pack(anchor="w")
            f_val = tk.Frame(card, bg="white")
            f_val.pack(fill="x", pady=5)
            tk.Label(f_val, text=valor, font=("Segoe UI", 18, "bold"), bg="white", fg=COR_TEXTO).pack(side="left")
            tk.Label(f_val, text=icon, font=("Segoe UI", 14), bg=cor_icon, fg="white", width=2).pack(side="right")
            tk.Label(card, text=subtexto, font=("Segoe UI", 8), bg="white", fg=COR_SUAVE).pack(anchor="w")
            return card

        card1 = criar_card(grid_cards, "VENDAS DO MÊS", f"R$ {self.dados['vendas_mes']:.2f}", "+0% em relação ao mês anterior", "🛍️", "#B794F4")
        card1.pack(side="left", padx=(0, 15), expand=True, fill="x")
        
        card2 = criar_card(grid_cards, "LUCRO DO MÊS", f"R$ {self.dados['lucro_mes']:.2f}", "+0% em relação ao mês anterior", "📈", "#68D391")
        card2.pack(side="left", padx=(0, 15), expand=True, fill="x")

        card3 = criar_card(grid_cards, "A RECEBER", f"R$ {self.dados['a_receber']:.2f}", "0 pagamentos pendentes", "💳", "#63B3ED")
        card3.pack(side="left", padx=(0, 15), expand=True, fill="x")

        card4 = criar_card(grid_cards, "PRODUTOS EM ESTOQUE", str(self.dados['total_estoque']), f"{self.dados['baixo_estoque']} itens com estoque baixo", "📦", "#F687B3")
        card4.pack(side="left", expand=True, fill="x")

        # Parte de Baixo
        grid_baixo = tk.Frame(corpo, bg=BG_APP)
        grid_baixo.pack(fill="both", expand=True, pady=20)

        card_pend = tk.Frame(grid_baixo, bg="white", padx=20, pady=15, highlightbackground="#E2E8F0", highlightthickness=1)
        card_pend.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        f_title_pend = tk.Frame(card_pend, bg="white")
        f_title_pend.pack(fill="x")
        tk.Label(f_title_pend, text="Contas pendentes", font=("Segoe UI", 14, "bold"), bg="white", fg=COR_TEXTO).pack(side="left")
        tk.Label(card_pend, text="Cobranças que precisam de atenção", font=("Segoe UI", 9), bg="white", fg=COR_SUAVE).pack(anchor="w", pady=(0, 15))

        if not self.dados['contas_pendentes']:
            tk.Label(card_pend, text="Nenhuma conta pendente.", font=("Segoe UI", 10, "italic"), bg="white", fg=COR_SUAVE).pack(pady=20)
        else:
            for conta in self.dados['contas_pendentes']:
                f_linha = tk.Frame(card_pend, bg="white", pady=10)
                f_linha.pack(fill="x")
                tk.Label(f_linha, text=f"👤 {conta['nome']}", font=("Segoe UI", 10, "bold"), bg="white", fg=COR_TEXTO).pack(side="left")
                tk.Label(f_linha, text=f"R$ {conta['valor']:.2f}", font=("Segoe UI", 10, "bold"), bg="white", fg=COR_TEXTO).pack(side="right")

        card_vendas = tk.Frame(grid_baixo, bg="white", padx=20, pady=15, highlightbackground="#E2E8F0", highlightthickness=1)
        card_vendas.pack(side="right", fill="both", expand=True)
        
        f_title_vend = tk.Frame(card_vendas, bg="white")
        f_title_vend.pack(fill="x")
        tk.Label(f_title_vend, text="Vendas recentes", font=("Segoe UI", 14, "bold"), bg="white", fg=COR_TEXTO).pack(side="left")
        tk.Label(card_vendas, text="Últimas movimentações registradas", font=("Segoe UI", 9), bg="white", fg=COR_SUAVE).pack(anchor="w", pady=(0, 15))

        if not self.dados['vendas_recentes']:
            tk.Label(card_vendas, text="Nenhuma venda registrada.", font=("Segoe UI", 10, "italic"), bg="white", fg=COR_SUAVE).pack(pady=20)
        else:
            for venda in self.dados['vendas_recentes']:
                f_linha = tk.Frame(card_vendas, bg="white", pady=5)
                f_linha.pack(fill="x")
                tk.Label(f_linha, text=f"👤 {venda['cliente']}\n📦 {venda['produto']}", font=("Segoe UI", 10, "bold"), bg="white", fg=COR_TEXTO, justify="left").pack(side="left")
                tk.Label(f_linha, text=f"R$ {venda['valor_final']:.2f}", font=("Segoe UI", 10, "bold"), bg="white", fg=COR_TEXTO).pack(side="right")