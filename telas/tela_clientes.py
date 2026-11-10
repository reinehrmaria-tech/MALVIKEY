import tkinter as tk
from tkinter import messagebox
from database import buscar_clientes, cadastrar_cliente
from telas.menu_lateral import MenuLateral
import datetime

BG_APP = "#F7F9FC"
COR_PRIMARIA = "#6C4EE3"
COR_TEXTO = "#2D3748"
COR_SUAVE = "#A0AEC0"
COR_BORDA = "#E2E8F0"

class TelaClientes:
    def __init__(self, root, nome_usuario):
        self.root = root
        self.nome_usuario = nome_usuario
        self.root.title("Essência Rústica - Clientes")
        self.root.configure(bg=BG_APP)
        self.root.state('zoomed')
        
        self.tela_atual = "lista" 
        self.renderizar()

    def limpar_tela(self):
        for w in self.root.winfo_children():
            w.destroy()

    def renderizar(self):
        self.limpar_tela()
        
        MenuLateral(self.root, "clientes")

        main_frame = tk.Frame(self.root, bg=BG_APP)
        main_frame.pack(side="right", fill="both", expand=True)

        header = tk.Frame(main_frame, bg="white", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Clientes", font=("Segoe UI", 12, "bold"), bg="white", fg=COR_TEXTO).pack(side="left", padx=30)
        tk.Label(header, text=f"👤 {self.nome_usuario}", font=("Segoe UI", 10, "bold"), bg="white", fg=COR_TEXTO).pack(side="right", padx=20)

        self.corpo = tk.Frame(main_frame, bg=BG_APP, padx=40, pady=20)
        self.corpo.pack(fill="both", expand=True)

        if self.tela_atual == "lista":
            self._tela_lista()
        else:
            self._tela_formulario()

    def _tela_lista(self):
        tk.Label(self.corpo, text="ESSÊNCIA RÚSTICA", font=("Segoe UI", 9, "bold"), bg=BG_APP, fg=COR_PRIMARIA).pack(anchor="w")
        tk.Label(self.corpo, text="Clientes", font=("Segoe UI", 24, "bold"), bg=BG_APP, fg=COR_TEXTO).pack(anchor="w")
        tk.Label(self.corpo, text="Consulte clientes e acompanhe a situação das vendas.", font=("Segoe UI", 10), bg=BG_APP, fg=COR_SUAVE).pack(anchor="w", pady=(0, 20))

        f_tools = tk.Frame(self.corpo, bg=BG_APP)
        f_tools.pack(fill="x", pady=10)

        f_search = tk.Frame(f_tools, bg="white", highlightbackground=COR_BORDA, highlightthickness=1)
        f_search.pack(side="left", fill="x", expand=True, ipady=5)
        tk.Label(f_search, text="🔍", bg="white", fg=COR_SUAVE).pack(side="left", padx=10)
        self.entry_busca = tk.Entry(f_search, font=("Segoe UI", 11), bg="white", bd=0, relief="flat")
        self.entry_busca.pack(side="left", fill="x", expand=True)
        self.entry_busca.insert(0, "Pesquisar cliente...")
        self.entry_busca.bind("<FocusIn>", self._limpar_busca)
        self.entry_busca.bind("<KeyRelease>", self._filtrar)

        btn_cad = tk.Button(f_tools, text="+ Cadastrar cliente", font=("Segoe UI", 10, "bold"), bg=COR_PRIMARIA, fg="white", bd=0, cursor="hand2", command=self._abrir_cadastro)
        btn_cad.pack(side="right", padx=(15, 0), ipadx=10, ipady=8)

        self.frame_tabela = tk.Frame(self.corpo, bg="white", highlightbackground=COR_BORDA, highlightthickness=1)
        self.frame_tabela.pack(fill="both", expand=True, pady=20)
        self._atualizar_tabela()

    def _atualizar_tabela(self, filtro=""):
        for w in self.frame_tabela.winfo_children():
            w.destroy()

        f_head = tk.Frame(self.frame_tabela, bg="#F7FAFC", pady=10)
        f_head.pack(fill="x")
        tk.Label(f_head, text="NOME", font=("Segoe UI", 9, "bold"), bg="#F7FAFC", fg=COR_SUAVE).pack(side="left", padx=30)
        tk.Label(f_head, text="CPF", font=("Segoe UI", 9, "bold"), bg="#F7FAFC", fg=COR_SUAVE).pack(side="left", padx=80)
        tk.Label(f_head, text="CIDADE", font=("Segoe UI", 9, "bold"), bg="#F7FAFC", fg=COR_SUAVE).pack(side="left", padx=80)

        clientes = buscar_clientes(filtro)
        if not clientes:
            tk.Label(self.frame_tabela, text="Nenhum cliente encontrado.", font=("Segoe UI", 11), bg="white", fg=COR_SUAVE).pack(pady=30)
            return

        for c in clientes:
            f_linha = tk.Frame(self.frame_tabela, bg="white", pady=15)
            f_linha.pack(fill="x")
            tk.Frame(f_linha, bg=COR_BORDA, height=1).pack(fill="x", side="bottom")

            tk.Label(f_linha, text=c['nome'], font=("Segoe UI", 10, "bold"), bg="white", fg=COR_TEXTO).pack(side="left", padx=30)
            tk.Label(f_linha, text=c['cpf'], font=("Segoe UI", 10), bg="white", fg=COR_TEXTO).pack(side="left", padx=95)
            tk.Label(f_linha, text=c['cidade'], font=("Segoe UI", 10), bg="white", fg=COR_TEXTO).pack(side="left", padx=80)

    def _filtrar(self, event=None):
        texto = self.entry_busca.get()
        if texto == "Pesquisar cliente...":
            return
        self._atualizar_tabela(texto)

    def _limpar_busca(self, event):
        if self.entry_busca.get() == "Pesquisar cliente...":
            self.entry_busca.delete(0, tk.END)

    def _abrir_cadastro(self):
        self.tela_atual = "form"
        self.renderizar()

    # --- FORMULÁRIO DE CADASTRO ---
    def _tela_formulario(self):
        tk.Label(self.corpo, text="CLIENTES", font=("Segoe UI", 9, "bold"), bg=BG_APP, fg=COR_PRIMARIA).pack(anchor="w")
        tk.Label(self.corpo, text="Cadastrar cliente", font=("Segoe UI", 24, "bold"), bg=BG_APP, fg=COR_TEXTO).pack(anchor="w")
        tk.Label(self.corpo, text="Preencha os dados abaixo para continuar.", font=("Segoe UI", 10), bg=BG_APP, fg=COR_SUAVE).pack(anchor="w", pady=(0, 20))

        card = tk.Frame(self.corpo, bg="white", padx=40, pady=30, highlightbackground=COR_BORDA, highlightthickness=1)
        card.pack(fill="x", anchor="w")
        
        # Grid configuration
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)

        def criar_campo(label_txt, row, col, width=45):
            f = tk.Frame(card, bg="white")
            f.grid(row=row, column=col, sticky="we", padx=15, pady=10)
            tk.Label(f, text=label_txt, font=("Segoe UI", 9, "bold"), bg="white", fg=COR_TEXTO).pack(anchor="w", pady=(0, 5))
            # width controla o tamanho, fill="none" impede de esticar
            entry = tk.Entry(f, font=("Segoe UI", 11), bg="#F9F9F9", bd=1, relief="solid", highlightthickness=1, highlightbackground=COR_BORDA, highlightcolor=COR_PRIMARIA, width=width)
            entry.pack(anchor="w", ipady=6) 
            return entry

        # Nome (maior) e CPF (menor)
        self.e_nome = criar_campo("Nome completo", 0, 0, width=55)
        self.e_cpf = criar_campo("CPF", 0, 1, width=25)
        self.e_cpf.insert(0, "   .   .   -  ") 
        self.e_cpf.bind("<KeyRelease>", self._mascara_cpf)
        self.e_cpf.bind("<FocusIn>", lambda e: self._limpar_mascara_vazia(self.e_cpf, "   .   .   -  "))

        # Telefone (menor) e Endereço (maior)
        self.e_tel = criar_campo("Telefone", 2, 0, width=25)
        self.e_tel.insert(0, "(  )     -    ") 
        self.e_tel.bind("<KeyRelease>", self._mascara_telefone)
        self.e_tel.bind("<FocusIn>", lambda e: self._limpar_mascara_vazia(self.e_tel, "(  )     -    "))
        
        self.e_end = criar_campo("Endereço", 2, 1, width=45)

        # Cidade (maior) e Data (menor)
        self.e_cidade = criar_campo("Cidade", 4, 0, width=40)
        
        f_data = tk.Frame(card, bg="white")
        f_data.grid(row=4, column=1, sticky="we", padx=15, pady=10)
        tk.Label(f_data, text="Data de cadastro", font=("Segoe UI", 9, "bold"), bg="white", fg=COR_TEXTO).pack(anchor="w", pady=(0, 5))
        e_data = tk.Entry(f_data, font=("Segoe UI", 11), bg="#EDF2F7", bd=1, relief="solid", fg=COR_SUAVE, width=20)
        e_data.pack(anchor="w", ipady=6)
        data_hoje = datetime.date.today().strftime('%d/%m/%Y')
        e_data.insert(0, f"{data_hoje}  📅")
        e_data.config(state="readonly")

        # Observação (largura total)
        f_obs = tk.Frame(card, bg="white")
        f_obs.grid(row=6, column=0, columnspan=2, sticky="we", padx=15, pady=10)
        tk.Label(f_obs, text="Observação", font=("Segoe UI", 9, "bold"), bg="white", fg=COR_TEXTO).pack(anchor="w", pady=(0, 5))
        self.e_obs = tk.Text(f_obs, font=("Segoe UI", 11), bg="#F9F9F9", height=3, bd=1, relief="solid", highlightthickness=1, highlightbackground=COR_BORDA, width=60)
        self.e_obs.pack(anchor="w")

        f_btns = tk.Frame(self.corpo, bg=BG_APP, pady=20)
        f_btns.pack(fill="x")
        
        btn_cancel = tk.Button(f_btns, text="Cancelar", font=("Segoe UI", 11, "bold"), bg="white", fg=COR_TEXTO, bd=1, relief="solid", cursor="hand2", command=self._cancelar_form)
        btn_cancel.pack(side="right", padx=10, ipadx=15, ipady=8)
        
        btn_salvar = tk.Button(f_btns, text="✓ Salvar", font=("Segoe UI", 11, "bold"), bg=COR_PRIMARIA, fg="white", bd=0, cursor="hand2", command=self._salvar_cliente)
        btn_salvar.pack(side="right", ipadx=15, ipady=8)

    # --- MÁSCARAS ---
    def _limpar_mascara_vazia(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def _mascara_cpf(self, event):
        if event.keysym in ['BackSpace', 'Delete', 'Left', 'Right', 'Tab']:
            return

        texto = self.e_cpf.get()
        numeros = "".join(filter(str.isdigit, texto))

        if len(numeros) > 11:
            numeros = numeros[:11]

        formatado = ""
        for i, num in enumerate(numeros):
            if i == 3 or i == 6: formatado += "."
            if i == 9: formatado += "-"
            formatado += num

        if texto != formatado:
            self.e_cpf.delete(0, tk.END)
            self.e_cpf.insert(0, formatado)

    def _mascara_telefone(self, event):
        if event.keysym in ['BackSpace', 'Delete', 'Left', 'Right', 'Tab']:
            return

        texto = self.e_tel.get()
        numeros = "".join(filter(str.isdigit, texto))

        if len(numeros) > 11:
            numeros = numeros[:11]

        formatado = ""
        for i, num in enumerate(numeros):
            if i == 0: formatado += "("
            if i == 2: formatado += ") "
            if i == 7: formatado += "-"
            formatado += num

        if texto != formatado:
            self.e_tel.delete(0, tk.END)
            self.e_tel.insert(0, formatado)

    def _cancelar_form(self):
        self.tela_atual = "lista"
        self.renderizar()

    def _salvar_cliente(self):
        nome = self.e_nome.get().strip()
        cpf = self.e_cpf.get().strip()
        tel = self.e_tel.get().strip()
        end = self.e_end.get().strip()
        cidade = self.e_cidade.get().strip()
        obs = self.e_obs.get("1.0", tk.END).strip()
        data_hoje = datetime.date.today().strftime('%Y-%m-%d')

        if "   .   .   -  " == cpf:
            cpf = ""

        if not nome or not cpf:
            messagebox.showwarning("Aviso", "Nome e CPF são obrigatórios!")
            return

        try:
            cadastrar_cliente(nome, cpf, tel, end, cidade, obs, data_hoje)
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.tela_atual = "lista"
            self.renderizar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")