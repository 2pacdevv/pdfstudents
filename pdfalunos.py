import tkinter as tk
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, Toplevel, Listbox
from PIL import Image, ImageTk
import sqlite3
from fpdf import FPDF

# Banco de dados SQLite
def criar_banco_de_dados():
    conn = sqlite3.connect('alunos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sala TEXT NOT NULL,
            foto_path TEXT NOT NULL,
            nota_prova1 REAL NOT NULL,
            nota_prova2 REAL NOT NULL,
            nota_trabalho REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

criar_banco_de_dados()

class Aluno:
    def __init__(self, nome, sala, foto_path, nota_prova1, nota_prova2, nota_trabalho):
        self.nome = nome
        self.sala = sala
        self.foto_path = foto_path
        self.nota_prova1 = nota_prova1
        self.nota_prova2 = nota_prova2
        self.nota_trabalho = nota_trabalho

    def calcular_media(self):
        media = (self.nota_prova1 * 2.5 + self.nota_prova2 * 2.5 + self.nota_trabalho * 2) / 7
        return round(media, 2)

    def exibir_informacoes(self):
        return (f"Nome: {self.nome}\n"
                f"Sala: {self.sala}\n"
                f"Nota Prova 1: {self.nota_prova1}\n"
                f"Nota Prova 2: {self.nota_prova2}\n"
                f"Nota Trabalho: {self.nota_trabalho}\n"
                f"Média: {self.calcular_media()}\n"
                f"Foto: {self.foto_path}")

    def salvar_no_banco(self):
        conn = sqlite3.connect('alunos.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alunos (nome, sala, foto_path, nota_prova1, nota_prova2, nota_trabalho)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.nome, self.sala, self.foto_path, self.nota_prova1, self.nota_prova2, self.nota_trabalho))
        conn.commit()
        conn.close()

def cadastrar_aluno():
    def salvar_aluno():
        nome = entry_nome.get()
        sala = entry_sala.get()
        foto_path = entry_foto_path.get()
        nota_prova1 = float(entry_nota_prova1.get())
        nota_prova2 = float(entry_nota_prova2.get())
        nota_trabalho = float(entry_nota_trabalho.get())

        aluno = Aluno(nome, sala, foto_path, nota_prova1, nota_prova2, nota_trabalho)
        aluno.salvar_no_banco()

        messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
        tela_de_cadastro.destroy()

    def selecionar_foto():
        caminho_foto = filedialog.askopenfilename(
            title="Selecione uma foto",
            filetypes=(("Arquivos de imagem", "*.jpg;*.jpeg;*.png"), ("Todos os arquivos", "*.*"))
        )
        if caminho_foto:
            entry_foto_path.delete(0, tk.END)
            entry_foto_path.insert(0, caminho_foto)

    tela_de_cadastro = Tk()
    tela_de_cadastro.title("Tela de Cadastro")
    tela_de_cadastro.config(bg="#1E1E1E")

    Label(tela_de_cadastro, text="Nome:", bg="#1E1E1E", fg="white").grid(row=0, column=0, padx=10, pady=5)
    entry_nome = Entry(tela_de_cadastro)
    entry_nome.grid(row=0, column=1, padx=10, pady=5)

    Label(tela_de_cadastro, text="Sala:", bg="#1E1E1E", fg="white").grid(row=1, column=0, padx=10, pady=5)
    entry_sala = Entry(tela_de_cadastro)
    entry_sala.grid(row=1, column=1, padx=10, pady=5)

    Label(tela_de_cadastro, text="Foto:", bg="#1E1E1E", fg="white").grid(row=2, column=0, padx=10, pady=5)
    entry_foto_path = Entry(tela_de_cadastro)
    entry_foto_path.grid(row=2, column=1, padx=10, pady=5)
    Button(tela_de_cadastro, text="Selecionar Foto", command=selecionar_foto).grid(row=2, column=2, padx=10, pady=5)

    Label(tela_de_cadastro, text="Nota Prova 1:", bg="#1E1E1E", fg="white").grid(row=3, column=0, padx=10, pady=5)
    entry_nota_prova1 = Entry(tela_de_cadastro)
    entry_nota_prova1.grid(row=3, column=1, padx=10, pady=5)

    Label(tela_de_cadastro, text="Nota Prova 2:", bg="#1E1E1E", fg="white").grid(row=4, column=0, padx=10, pady=5)
    entry_nota_prova2 = Entry(tela_de_cadastro)
    entry_nota_prova2.grid(row=4, column=1, padx=10, pady=5)

    Label(tela_de_cadastro, text="Nota Trabalho:", bg="#1E1E1E", fg="white").grid(row=5, column=0, padx=10, pady=5)
    entry_nota_trabalho = Entry(tela_de_cadastro)
    entry_nota_trabalho.grid(row=5, column=1, padx=10, pady=5)

    Button(tela_de_cadastro, text="Salvar", command=salvar_aluno).grid(row=6, column=1, pady=20)

    tela_de_cadastro.mainloop()

def listar_alunos():
    def selecionar_aluno():
        selecionado = listbox.curselection()
        if selecionado:
            aluno_id = lista_alunos[selecionado[0]][0]
            gerar_pdf(aluno_id)
            tela_listagem.destroy()

    conn = sqlite3.connect('alunos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome FROM alunos')
    lista_alunos = cursor.fetchall()
    conn.close()

    tela_listagem = Toplevel()
    tela_listagem.title("Lista de Alunos")
    tela_listagem.config(bg="#1E1E1E")

    listbox = Listbox(tela_listagem, bg="#2c2c2c", fg="white", font=("Arial", 12))
    listbox.pack(padx=20, pady=20, fill="both", expand=True)

    for aluno in lista_alunos:
        listbox.insert(tk.END, aluno[1])

    Button(tela_listagem, text="Selecionar", command=selecionar_aluno).pack(pady=10)

def gerar_pdf(aluno_id):
    conn = sqlite3.connect('alunos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alunos WHERE id = ?', (aluno_id,))
    aluno = cursor.fetchone()
    conn.close()

    if aluno:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Informações do Aluno", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Nome: {aluno[1]}", ln=True)
        pdf.cell(200, 10, txt=f"Sala: {aluno[2]}", ln=True)
        pdf.cell(200, 10, txt=f"Nota Prova 1: {aluno[4]}", ln=True)
        pdf.cell(200, 10, txt=f"Nota Prova 2: {aluno[5]}", ln=True)
        pdf.cell(200, 10, txt=f"Nota Trabalho: {aluno[6]}", ln=True)
        pdf.cell(200, 10, txt=f"Média: {(aluno[4] * 2.5 + aluno[5] * 2.5 + aluno[6] * 2) / 7}", ln=True)
        pdf.output(f"aluno_{aluno[1]}.pdf")
        messagebox.showinfo("Sucesso", f"PDF gerado com sucesso: aluno_{aluno[1]}.pdf")

def tela_inicial():
    tela_inicial = Tk()
    tela_inicial.title("Inicio")
    is_fullscreen = True
    tela_inicial.attributes("-fullscreen", is_fullscreen)
    tela_inicial.config(bg="#1E1E1E")

    btn_cadastrar_aluno = Button(tela_inicial, text="Cadastrar Aluno", command=cadastrar_aluno)
   
    btn_listar_alunos = Button(tela_inicial, text="Listar Alunos", command=listar_alunos)
    btn_listar_alunos.pack(pady=20)

    tela_inicial.mainloop()

tela_inicial()