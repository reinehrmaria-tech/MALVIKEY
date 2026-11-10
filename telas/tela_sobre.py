"""Tela Sobre (exemplo de outra tela do sistema)."""

import tkinter as tk

from config import APP_TITLE, APP_VERSION


class TelaSobre:
    def __init__(self, root: tk.Tk, dados_usuario: dict):
        self.root = root
        self.dados_usuario = dados_usuario

        self.root.title(f"{APP_TITLE} - Sobre")
        self.root.geometry("500x350")
        self.root.configure(bg="#f0f0f0")

        self._montar_widgets()

    def _montar_widgets(self):
        tk.Label(
            self.root, text=f"Sobre o {APP_TITLE}", font=("Arial", 18, "bold"),
            bg="#f0f0f0", fg="#2c3e50"
        ).pack(pady=(30, 10))

        tk.Label(
            self.root,
            text=(f"{APP_TITLE} v{APP_VERSION}\n\n"
                  "Sistema de demonstração com login e múltiplas telas.\n"
                  "Construído com Python + Tkinter + MySQL."),
            font=("Arial", 11), bg="#f0f0f0", fg="#34495e", justify="center"
        ).pack(pady=10)

        tk.Label(
            self.root, text=f"Usuário logado: {self.dados_usuario['usuario']}",
            font=("Arial", 10, "italic"), bg="#f0f0f0", fg="#7f8c8d"
        ).pack(pady=10)

        tk.Button(
            self.root, text="← Voltar", font=("Arial", 11, "bold"),
            bg="#3498db", fg="white", cursor="hand2", width=15,
            command=self._voltar
        ).pack(pady=25)

    def _voltar(self):
        for w in self.root.winfo_children():
            w.destroy()
        from telas.tela_inicial import TelaInicial
        TelaInicial(self.root, self.dados_usuario)