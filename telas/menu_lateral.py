import tkinter as tk
from PIL import Image, ImageTk

class MenuLateral(tk.Frame):
    def __init__(self, root, tela_atual):
        super().__init__(root, bg="white", width=240)
        self.pack(side="left", fill="y")
        self.pack_propagate(False)
        self.root = root
        self.tela_atual = tela_atual

        # Carrega a Logo (aumentada para 60x60)
        try:
            img_pil = Image.open("logo.png").resize((60, 60), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img_pil)
            tk.Label(self, image=self.logo_img, bg="white").pack(pady=(30, 10))
        except Exception:
            tk.Label(self, text="[LOGO]", font=("Segoe UI", 10), bg="white", fg="red").pack(pady=(30, 10))

        # Nome em duas linhas
        tk.Label(self, text="Essência\nRústica", font=("Georgia", 20, "bold"), bg="white", fg="#2D3748", justify="center").pack(pady=(0, 40))

        # Botões
        self._criar_botao("🏠  Início", "inicio")
        self._criar_botao("👥  Clientes", "clientes")
        self._criar_botao("🛍️  Produtos", "produtos")
        self._criar_botao("📄  Nova venda", "nova_venda")
        self._criar_botao("💳  Contas a receber", "contas")
        self._criar_botao("📊  Relatórios", "relatorios")

        # Sair
        btn_sair = tk.Label(self, text="🚪  Sair", font=("Segoe UI", 11), bg="white", fg="#E53E3E", cursor="hand2")
        btn_sair.pack(side="bottom", anchor="w", padx=20, pady=20)
        btn_sair.bind("<Button-1>", lambda e: self._navegar("sair"))

    def _criar_botao(self, texto, tela_destino):
        ativo = (self.tela_atual == tela_destino)
        cor_fundo = "#F3E8FF" if ativo else "white"
        cor_texto = "#6C4EE3" if ativo else "#2D3748"
        fonte = ("Segoe UI", 11, "bold") if ativo else ("Segoe UI", 11)
        
        btn = tk.Label(self, text=texto, font=fonte, bg=cor_fundo, fg=cor_texto, anchor="w", padx=20, pady=12, cursor="hand2")
        btn.pack(fill="x", pady=2)
        btn.bind("<Button-1>", lambda e: self._navegar(tela_destino))
        
        if not ativo:
            btn.bind("<Enter>", lambda e: btn.config(bg="#EDF2F7"))
            btn.bind("<Leave>", lambda e: btn.config(bg="white"))

    def _navegar(self, destino):
        for w in self.root.winfo_children():
            w.destroy()
        
        nome_usuario = "Admin"
        
        if destino == "inicio":
            from telas.tela_inicial import TelaInicial
            TelaInicial(self.root, {'usuario': nome_usuario})
        elif destino == "clientes":
            from telas.tela_clientes import TelaClientes
            TelaClientes(self.root, nome_usuario)
        elif destino == "sair":
            from telas.tela_login import TelaLogin
            TelaLogin(self.root)
        else:
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Em breve", "Esta tela ainda será construída.")
            from telas.tela_inicial import TelaInicial
            TelaInicial(self.root, {'usuario': nome_usuario})