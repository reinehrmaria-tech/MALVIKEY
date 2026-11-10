"""Ponto de entrada do sistema Malvikey."""

import tkinter as tk
from telas.tela_login import TelaLogin


def main():
    root = tk.Tk()
    TelaLogin(root)
    root.mainloop()


if __name__ == "__main__":
    main()