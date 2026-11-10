"""Tela de login — Estilo moderno com logo e fontes refinadas."""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from auth import autenticar

# ============ PALETA DE CORES ============
COR_FUNDO        = "#F3F4FB"
COR_CARD         = "#FFFFFF"
COR_PRIMARIA     = "#6C4EE3"
COR_PRIMARIA_HOV = "#5B3FD1"
COR_TEXTO        = "#1E1E1E"
COR_TEXTO_SUAVE  = "#777777"
COR_BORDA        = "#E0E0E0"
COR_AZUL_CLARO   = "#DCE6FA"
COR_ROXO_CLARO   = "#E2D9F9"

class TelaLogin:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Login - Essência Rústica")
        self.root.geometry("900x600")
        self.root.configure(bg=COR_FUNDO)
        
        # Bloqueia redimensionamento e maximização
        self.root.resizable(False, False)
        
        # Centraliza a janela no meio do monitor
        self.root.eval("tk::PlaceWindow . center")

        self._montar_fundo_e_card()

    def _montar_fundo_e_card(self):
        # Canvas para os círculos de fundo
        self.canvas = tk.Canvas(self.root, width=900, height=600, bg=COR_FUNDO, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Círculos decorativos
        self.canvas.create_oval(-250, 400, 350, 1000, fill=COR_AZUL_CLARO, outline="")
        self.canvas.create_oval(600, -200, 1150, 350, fill=COR_ROXO_CLARO, outline="")

        # Card Central
        self.card = tk.Frame(self.canvas, bg=COR_CARD, padx=45, pady=40)
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # ---- Cabeçalho (Logo e Nome) ----
        header_frame = tk.Frame(self.card, bg=COR_CARD)
        header_frame.pack(fill="x", pady=(0, 30))

        # Carrega a imagem da logo
        try:
            img_pil = Image.open("logo.png").resize((45, 45), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img_pil)
            lbl_logo = tk.Label(header_frame, image=self.logo_img, bg=COR_CARD)
            lbl_logo.pack(side="left", padx=(0, 15))
        except Exception:
            tk.Label(header_frame, text="[LOGO]", font=("Segoe UI", 10), bg=COR_CARD, fg="red").pack(side="left", padx=(0, 15))

        title_frame = tk.Frame(header_frame, bg=COR_CARD)
        title_frame.pack(side="left")
        
        # Fonte alterada para Georgia (remete ao rústico/elegante)
        tk.Label(title_frame, text="Essência Rústica", font=("Georgia", 22, "bold"), bg=COR_CARD, fg=COR_TEXTO).pack(anchor="w")
        tk.Label(title_frame, text="Gestão para o seu negócio", font=("Segoe UI", 10), bg=COR_CARD, fg=COR_TEXTO_SUAVE).pack(anchor="w")

        # ---- Títulos ----
        tk.Label(self.card, text="Bem-vinda de volta", font=("Segoe UI", 20, "bold"), bg=COR_CARD, fg=COR_TEXTO).pack(pady=(5, 5))
        tk.Label(self.card, text="Entre para gerenciar seu negócio", font=("Segoe UI", 10), bg=COR_CARD, fg=COR_TEXTO_SUAVE).pack(pady=(0, 25))

        # ---- Campo Usuário ----
        tk.Label(self.card, text="Usuário ou e-mail", font=("Segoe UI", 9, "bold"), bg=COR_CARD, fg=COR_TEXTO).pack(anchor="w", pady=(0, 5))
        
        self.entry_usuario = tk.Entry(
            self.card, font=("Segoe UI", 11), bd=1, relief="solid", 
            highlightthickness=1, highlightbackground=COR_BORDA, highlightcolor=COR_PRIMARIA,
            bg="#F9F9F9", fg=COR_TEXTO
        )
        self.entry_usuario.pack(fill="x", ipady=8, pady=(0, 15))
        
        # Preenche com o usuário padrão por conveniência
        self.entry_usuario.insert(0, "rosmari@123")
        self.entry_usuario.config(fg=COR_TEXTO_SUAVE)
        self.entry_usuario.bind("<FocusIn>", lambda e: self._limpar_placeholder(e, "rosmari@123"))
        self.entry_usuario.bind("<FocusOut>", lambda e: self._add_placeholder(e, "rosmari@123"))

        # ---- Campo Senha ----
        tk.Label(self.card, text="Senha", font=("Segoe UI", 9, "bold"), bg=COR_CARD, fg=COR_TEXTO).pack(anchor="w", pady=(0, 5))
        
        self.entry_senha = tk.Entry(
            self.card, font=("Segoe UI", 11), bd=1, relief="solid", show="*",
            highlightthickness=1, highlightbackground=COR_BORDA, highlightcolor=COR_PRIMARIA,
            bg="#F9F9F9", fg=COR_TEXTO
        )
        self.entry_senha.pack(fill="x", ipady=8, pady=(0, 25))

        # ---- Botão Entrar ----
        self.btn_entrar = tk.Button(
            self.card, text="Entrar  →", font=("Segoe UI", 11, "bold"),
            bg=COR_PRIMARIA, fg="white", activebackground=COR_PRIMARIA_HOV, activeforeground="white",
            bd=0, relief="flat", cursor="hand2", command=self._fazer_login
        )
        self.btn_entrar.pack(fill="x", ipady=8)
        
        self.btn_entrar.bind("<Enter>", lambda e: self.btn_entrar.configure(bg=COR_PRIMARIA_HOV))
        self.btn_entrar.bind("<Leave>", lambda e: self.btn_entrar.configure(bg=COR_PRIMARIA))

        # ---- Links e Rodapé ----
        link_frame = tk.Frame(self.card, bg=COR_CARD)
        link_frame.pack(pady=(20, 0))
        
        tk.Label(link_frame, text="Não tem uma conta? ", font=("Segoe UI", 9), bg=COR_CARD, fg=COR_TEXTO_SUAVE).pack(side="left")
        
        # Link para o Cadastro
        lbl_cadastrar = tk.Label(link_frame, text="Cadastrar-se", font=("Segoe UI", 9, "bold"), bg=COR_CARD, fg=COR_PRIMARIA, cursor="hand2")
        lbl_cadastrar.pack(side="left")
        lbl_cadastrar.bind("<Button-1>", lambda e: self._abrir_cadastro())

        # Rodapé alterado
        tk.Label(self.card, text="Sistema de controle de vendas Essência Rústica", font=("Segoe UI", 8), bg=COR_CARD, fg="#AAAAAA").pack(pady=(25, 0))

        # Atalhos de teclado
        self.root.bind("<Return>", lambda e: self._fazer_login())

    # ---- Helpers para Placeholder ----
    def _limpar_placeholder(self, event, texto):
        if event.widget.get() == texto:
            event.widget.delete(0, tk.END)
            event.widget.config(fg=COR_TEXTO)

    def _add_placeholder(self, event, texto):
        if not event.widget.get():
            event.widget.insert(0, texto)
            event.widget.config(fg=COR_TEXTO_SUAVE)

    # ---- Lógica de Login ----
    def _fazer_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        if usuario == "rosmari@123" and senha == "":
            messagebox.showwarning("Atenção", "Preencha a senha para continuar.")
            return

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Preencha usuário e senha!")
            return

        try:
            dados = autenticar(usuario, senha)
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            return

        if dados:
            for w in self.root.winfo_children():
                w.destroy()
            from telas.tela_inicial import TelaInicial
            TelaInicial(self.root, dados)
        else:
            messagebox.showerror("Acesso Negado", "Usuário ou senha incorretos.")
            self.entry_senha.delete(0, tk.END)
            self.entry_senha.focus()

    # ---- Navegação ----
    def _abrir_cadastro(self):
        for w in self.root.winfo_children():
            w.destroy()
        from telas.tela_cadastro import TelaCadastro
        TelaCadastro(self.root)