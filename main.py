import customtkinter as ctk
import tkinter.messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

cores = {
    "dark": {
        "bg": "#1e1e1e", "text": "#ffffff", "frame": "#292929",
        "entry": "#333333", "btn": "#3a7ebf", "btn_hover": "#4a90e2"
    },
    "light": {
        "bg": "#f5f5f5", "text": "#000000", "frame": "#ffffff",
        "entry": "#e0e0e0", "btn": "#0078d7", "btn_hover": "#00aaff"
    },
}

def get_cor(tipo):
    tema = ctk.get_appearance_mode().lower()
    return cores["dark" if tema == "dark" else "light"][tipo]

categorias = []
valores = []
orcamento_maximo = 0

def salvar_dados():
    if not categorias or not valores:
        tkinter.messagebox.showinfo("Aviso", "Nenhum dado inserido.")
        return

    caminho = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Texto", "*.txt")],
        title="Salvar como"
    )
    if not caminho:
        return

    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(f"{orcamento_maximo}\n")
            for cat, val in zip(categorias, valores):
                f.write(f"{cat};{val}\n")
        tkinter.messagebox.showinfo("Sucesso", "Dados salvos.")
    except Exception as e:
        tkinter.messagebox.showerror("Erro", f"Falha ao salvar: {e}")

def carregar_dados():
    global orcamento_maximo
    caminho = filedialog.askopenfilename(
        title="Selecionar arquivo",
        filetypes=[("Texto", "*.txt")]
    )
    if not caminho:
        return

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        categorias.clear()
        valores.clear()
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        orcamento_maximo = float(linhas[0].strip())
        orcamento_label.configure(text=f"Orçamento definido: R$ {orcamento_maximo:.2f}")

        for linha in linhas[1:]:
            if ";" in linha:
                cat, val = linha.strip().split(";")
                categorias.append(cat)
                valores.append(float(val))
                ctk.CTkLabel(
                    scrollable_frame,
                    text=f"{cat}: R$ {float(val):.2f}",
                    text_color=get_cor("text")
                ).pack(anchor="w", padx=10)

        atualizar_resumo()
        tkinter.messagebox.showinfo("Sucesso", "Dados carregados.")
    except Exception as e:
        tkinter.messagebox.showerror("Erro", f"Falha ao carregar: {e}")

def definir_orcamento():
    global orcamento_maximo
    texto = orcamento_entry.get().replace(",", ".")
    try:
        orcamento_maximo = float(texto)
        orcamento_label.configure(text=f"Orçamento definido: R$ {orcamento_maximo:.2f}")
        orcamento_entry.delete(0, "end")
        atualizar_resumo()
    except ValueError:
        tkinter.messagebox.showerror("Erro", "Valor inválido.")

def calcular_total_gasto():
    return sum(valores)

def atualizar_resumo():
    total = calcular_total_gasto()
    restante = orcamento_maximo - total
    resumo_label.configure(text=f"Total gasto: R$ {total:.2f} | Restante: R$ {restante:.2f}")
    if restante < 0:
        tkinter.messagebox.showwarning("Atenção", "Orçamento ultrapassado.")

def adicionar_gasto():
    descricao = gasto_entry.get()
    valor_texto = valor_entry.get().replace(",", ".")

    if not descricao:
        tkinter.messagebox.showwarning("Aviso", "Informe a descrição.")
        return

    try:
        valor = float(valor_texto)
    except ValueError:
        tkinter.messagebox.showerror("Erro", "Valor inválido.")
        return

    categorias.append(descricao)
    valores.append(valor)

    ctk.CTkLabel(
        scrollable_frame,
        text=f"{descricao}: R$ {valor:.2f}",
        text_color=get_cor("text")
    ).pack(anchor="w", padx=10)

    gasto_entry.delete(0, "end")
    valor_entry.delete(0, "end")
    atualizar_resumo()

def gerar_grafico():
    if not categorias:
        tkinter.messagebox.showinfo("Aviso", "Nenhum dado para gerar gráfico.")
        return

    tema = ctk.get_appearance_mode().lower()
    fundo = "#1e1e1e" if tema == "dark" else "#ffffff"
    texto = "#ffffff" if tema == "dark" else "#000000"

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        valores,
        labels=categorias,
        autopct="%.1f%%",
        startangle=140,
        textprops={"color": texto, "fontsize": 10},
        wedgeprops={"linewidth": 1, "edgecolor": fundo}
    )
    ax.set_title("Distribuição de Gastos", fontsize=14, fontweight="bold", color=texto)
    fig.patch.set_facecolor(fundo)

    grafico_window = ctk.CTkToplevel(janela)
    grafico_window.title("Gráfico")
    grafico_window.geometry("700x500")
    grafico_window.configure(fg_color=get_cor("bg"))

    canvas = FigureCanvasTkAgg(fig, master=grafico_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Controle de Gastos")
janela.geometry("850x650")
janela.configure(fg_color=get_cor("bg"))

title_label = ctk.CTkLabel(
    janela,
    text="Controle de Gastos Pessoais",
    font=("Roboto", 26, "bold"),
    text_color=get_cor("text")
)
title_label.pack(pady=10)

orcamento_frame = ctk.CTkFrame(janela, fg_color=get_cor("frame"))
orcamento_frame.pack(pady=10, padx=30, fill="x")

orcamento_entry = ctk.CTkEntry(
    orcamento_frame,
    placeholder_text="Orçamento total (R$)",
    fg_color=get_cor("entry"),
    width=200,
    height=40
)
orcamento_entry.grid(row=0, column=0, padx=10, pady=10)

botao_orcamento = ctk.CTkButton(
    orcamento_frame,
    text="Definir Orçamento",
    command=definir_orcamento,
    fg_color=get_cor("btn"),
    hover_color=get_cor("btn_hover"),
    font=("Helvetica", 12, "bold")
)
botao_orcamento.grid(row=0, column=1, padx=10, pady=10)

orcamento_label = ctk.CTkLabel(
    orcamento_frame,
    text="Orçamento não definido",
    text_color=get_cor("text"),
    font=("Helvetica", 12, "bold")
)
orcamento_label.grid(row=0, column=2, padx=10)

entrada_frame = ctk.CTkFrame(janela, fg_color=get_cor("frame"))
entrada_frame.pack(pady=10, padx=30, fill="x")

gasto_entry = ctk.CTkEntry(
    entrada_frame,
    placeholder_text="Categoria",
    fg_color=get_cor("entry"),
    width=200,
    height=40
)
gasto_entry.grid(row=0, column=0, padx=10, pady=10)

valor_entry = ctk.CTkEntry(
    entrada_frame,
    placeholder_text="Valor (R$)",
    fg_color=get_cor("entry"),
    width=200,
    height=40
)
valor_entry.grid(row=0, column=1, padx=10, pady=10)

botao_adicionar = ctk.CTkButton(
    entrada_frame,
    text="Adicionar Gasto",
    command=adicionar_gasto,
    fg_color=get_cor("btn"),
    hover_color=get_cor("btn_hover"),
    font=("Helvetica", 12, "bold")
)
botao_adicionar.grid(row=0, column=2, padx=10, pady=10)

botao_grafico = ctk.CTkButton(
    entrada_frame,
    text="Gerar Gráfico",
    command=gerar_grafico,
    fg_color="#00aa77",
    hover_color="#00cc99",
    font=("Helvetica", 12, "bold")
)
botao_grafico.grid(row=0, column=3, padx=10, pady=10)

resumo_label = ctk.CTkLabel(
    janela,
    text="Total gasto: R$ 0.00 | Restante: R$ 0.00",
    text_color=get_cor("text"),
    font=("Helvetica", 13, "bold")
)
resumo_label.pack(pady=5)

scrollable_frame = ctk.CTkScrollableFrame(
    janela, fg_color=get_cor("frame"), width=600, height=250
)
scrollable_frame.pack(pady=20, padx=30, fill="both", expand=True)

acoes_frame = ctk.CTkFrame(janela, fg_color=get_cor("frame"))
acoes_frame.pack(pady=10, padx=30, fill="x")

botao_salvar = ctk.CTkButton(
    acoes_frame,
    text="Salvar Dados",
    command=salvar_dados,
    fg_color="#4588cc",
    hover_color="#5699dd",
    font=("Helvetica", 12, "bold")
)
botao_salvar.grid(row=0, column=0, padx=10, pady=10)

botao_carregar = ctk.CTkButton(
    acoes_frame,
    text="Carregar Dados",
    command=carregar_dados,
    fg_color="#888844",
    hover_color="#999955",
    font=("Helvetica", 12, "bold")
)
botao_carregar.grid(row=0, column=1, padx=10, pady=10)

janela.mainloop()
