"""Tela de cadastro de novos usuários."""

import tkinter as tk
from tkinter import messagebox
import re
from database import cadastrar_usuario

# Cores no mesmo padrão do Login
COR_FUNDO        = "#F3F4FB"
COR_CARD         = "#FFFFFF"
COR_PRIMARIA     = "#6C4EE3"
COR_PRIMARIA_HOV = "#5B3FD1"
COR_TEXTO        = "#1E1E1E"
COR_TEXTO_SUAVE  = "#777777"
COR_BORDA        = "#E0E0E0"
COR_AZUL_CLARO   = "#DCE6FA"
COR_ROXO_CLARO   = "#E2D9F9"

class TelaCadastro:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Cadastro - Essência Rústica")
        self.root.geometry("900x650") # Um pouco mais alta para caber os campos
        self.root.configure(bg=COR_FUNDO)
        self.root.resizable(False, False)
        self.root.eval("tk::PlaceWindow . center")

        self._montar_fundo_e_card()

    def _montar_fundo_e_card(self):
        self.canvas = tk.Canvas(self.root, width=900, height=650, bg=COR_FUNDO, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_oval(-250, 400, 350, 1000, fill=COR_AZUL_CLARO, outline="")
        self.canvas.create_oval(600, -200, 1150, 350, fill=COR_ROXO_CLARO, outline="")

        self.card = tk.Frame(self.canvas, bg=COR_CARD, padx=45, pady=35)
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # ---- Títulos ----
        tk.Label(self.card, text="Criar uma conta", font=("Segoe UI", 20, "bold"), bg=COR_CARD, fg=COR_TEXTO).pack(pady=(0, 5))
        tk.Label(self.card, text="Preencha os dados abaixo para se cadastrar", font=("Segoe UI", 10), bg=COR_CARD, fg=COR_TEXTO_SUAVE).pack(pady=(0, 25))

        # ---- Campo Usuário ----
        tk.Label(self.card, text="Usuário", font=("Segoe UI", 9, "bold"), bg=COR_CARD, fg=COR_TEXTO).pack(anchor="w", pady=(0, 5))
        
        self.entry_usuario = tk.Entry(
            self.card, font=("Segoe UI", 11), bd=1, relief="solid", 
            highlightthickness=1, highlightbackground=COR_BORDA, highlightcolor=COR_PRIMARIA,
            bg="#F9F9F9", fg=COR_TEXTO
        )
        self.entry_usuario.pack(fill="x", ipady=8, pady=(0, 5))
        
        tk.Label(self.card, text="Sem espaços, deve conter número e caractere especial (ex: @, #, !, .)", 
                 font=("Segoe UI", 8), bg=COR_CARD, fg=COR_TEXTO_SUAVE).pack(anchor="w", pady=(0, 15))

        # ---- Campo Senha ----
        tk.Label(self.card, text="Senha", font=("Segoe UI", 9, "bold"), bg=COR_CARD, fg=COR_TEXTO).pack(anchor="w", pady=(0, 5))
        self.entry_senha = tk.Entry(
            self.card, font=("Segoe UI", 11), bd=1, relief="solid", show="*",
            highlightthickness=1, highlightbackground=COR_BORDA, highlightcolor=COR_PRIMARIA,
            bg="#F9F9F9", fg=COR_TEXTO
        )
        self.entry_senha.pack(fill="x", ipady=8, pady=(0, 5))

        # Texto de ajuda atualizado (sem exigir caractere especial)
        tk.Label(self.card, text="Mínimo 8 caracteres, contendo letras maiúsculas, minúsculas e números.", 
                 font=("Segoe UI", 8), bg=COR_CARD, fg=COR_TEXTO_SUAVE).pack(anchor="w", pady=(0, 15))

        # ---- Confirmar Senha ----
        tk.Label(self.card, text="Confirmar Senha", font=("Segoe UI", 9, "bold"), bg=COR_CARD, fg=COR_TEXTO).pack(anchor="w", pady=(0, 5))
        self.entry_confirmar = tk.Entry(
            self.card, font=("Segoe UI", 11), bd=1, relief="solid", show="*",
            highlightthickness=1, highlightbackground=COR_BORDA, highlightcolor=COR_PRIMARIA,
            bg="#F9F9F9", fg=COR_TEXTO
        )
        self.entry_confirmar.pack(fill="x", ipady=8, pady=(0, 25))

        # ---- Botão Cadastrar ----
        self.btn_cadastrar = tk.Button(
            self.card, text="Cadastrar", font=("Segoe UI", 11, "bold"),
            bg=COR_PRIMARIA, fg="white", activebackground=COR_PRIMARIA_HOV, activeforeground="white",
            bd=0, relief="flat", cursor="hand2", command=self._realizar_cadastro
        )
        self.btn_cadastrar.pack(fill="x", ipady=8)
        
        self.btn_cadastrar.bind("<Enter>", lambda e: self.btn_cadastrar.configure(bg=COR_PRIMARIA_HOV))
        self.btn_cadastrar.bind("<Leave>", lambda e: self.btn_cadastrar.configure(bg=COR_PRIMARIA))

        # ---- Voltar ao Login ----
        link_frame = tk.Frame(self.card, bg=COR_CARD)
        link_frame.pack(pady=(20, 0))
        
        tk.Label(link_frame, text="Já tem uma conta? ", font=("Segoe UI", 9), bg=COR_CARD, fg=COR_TEXTO_SUAVE).pack(side="left")
        lbl_voltar = tk.Label(link_frame, text="Voltar para o Login", font=("Segoe UI", 9, "bold"), bg=COR_CARD, fg=COR_PRIMARIA, cursor="hand2")
        lbl_voltar.pack(side="left")
        lbl_voltar.bind("<Button-1>", lambda e: self._voltar_login())

        self.root.bind("<Return>", lambda e: self._realizar_cadastro())

    def _realizar_cadastro(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()
        confirmar = self.entry_confirmar.get().strip()

        # 1. Validação do Usuário
        if " " in usuario:
            messagebox.showerror("Erro", "O usuário não pode conter espaços.")
            return
        
        if not re.search(r'[0-9]', usuario):
            messagebox.showerror("Erro", "O usuário precisa conter pelo menos um número.")
            return
            
        if not re.search(r'[^a-zA-Z0-9]', usuario):
            messagebox.showerror("Erro", "O usuário precisa conter pelo menos um caractere especial (ex: @, ., _).")
            return

        # 2. Validação da Senha Forte (Nova Regra: Sem obrigatoriedade de caractere especial)
        if len(senha) < 8:
            messagebox.showerror("Erro", "A senha deve ter no mínimo 8 caracteres.")
            return
        if not re.search(r'[A-Z]', senha) or not re.search(r'[a-z]', senha) or not re.search(r'[0-9]', senha):
            messagebox.showerror("Erro", "A senha deve conter letras maiúsculas, minúsculas e números.")
            return

        # 3. Confirmação de Senha
        if senha != confirmar:
            messagebox.showerror("Erro", "As senhas não coincidem. Tente novamente.")
            self.entry_confirmar.delete(0, tk.END)
            self.entry_confirmar.focus()
            return

        # 4. Salvar no Banco
        try:
            sucesso = cadastrar_usuario(usuario, senha)
            if sucesso:
                messagebox.showinfo("Sucesso", "Conta criada com sucesso! Faça login para entrar.")
                self._voltar_login()
            else:
                messagebox.showerror("Erro", "Este usuário já está cadastrado no sistema.")
        except Exception as e:
            messagebox.showerror("Erro Crítico", str(e))

    def _voltar_login(self):
        for w in self.root.winfo_children():
            w.destroy()
        from telas.tela_login import TelaLogin
        TelaLogin(self.root)