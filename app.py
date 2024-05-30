import tkinter as tk
from tkinter import messagebox as mb
import sqlite3
import re 

connection = sqlite3.connect("teste.db")
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Matricula (
                    nome TEXT,
                    cpf TEXT,
                    estado TEXT,
                    curso TEXT
                )''')

def ler_estados():
    with open('config.txt', 'r') as file:
        conteudo = file.read()
        estados = conteudo.split(';')
    return [estado.strip() for estado in estados]

def VerificarCPF(CPF):
    padrao = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
    if re.match(padrao,CPF):
        return True
    else:
        return False

def salvar_dados():
    global entry_nome, entry_cpf, entry_estado, entry_curso
    
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    estado = entry_estado.get()
    curso = entry_curso.get()

    if not VerificarCPF(cpf):
        mb.showerror("Erro", "CPF inválido")
        return

    estados_lista = ler_estados()
    if estado not in estados_lista:
        mb.showerror("Erro", "Estado inválido")
        return

    cursor.execute("INSERT INTO Matricula VALUES (?, ?, ?, ?)", (nome, cpf, estado, curso))
    connection.commit()
    mb.showinfo("Sucesso", "Dados salvos com sucesso!")

def mostrar_dados():
    rows = cursor.execute("SELECT * FROM Matricula").fetchall()
    
    dados_window = tk.Toplevel()
    dados_window.title("Dados Salvos")
    dados_window.geometry("400x300")

    text_area = tk.Text(dados_window)
    text_area.pack(expand=True, fill='both')

    for row in rows:
        text_area.insert(tk.END, f"Nome: {row[0]}, CPF: {row[1]}, Estado: {row[2]}, Curso: {row[3]}\n")

def Main():
    global entry_nome, entry_cpf, entry_estado, entry_curso

    root = tk.Tk()
    root.title("Aplicativo UNISTARS")
    root.resizable(True, True)
    root.geometry("800x600")

    bg_photo = tk.PhotoImage(file="bt21.png")

    background_label = tk.Label(root, image=bg_photo)
    background_label.place(relwidth=1, relheight=1)

    titulo_label = tk.Label(root, text="Bem-vindo ao Unistars!", background="pink" , font=("Helvetica", 20))
    titulo_label.place(relx=0.5, rely=0.1, anchor="center")

    label_nome = tk.Label(root, text="Nome")
    label_nome.place(relx=0.3, rely=0.3, anchor="center")
    entry_nome = tk.Entry(root)
    entry_nome.place(relx=0.5, rely=0.3, anchor="center")

    label_estado = tk.Label(root, text="Estado")
    label_estado.place(relx=0.3, rely=0.4, anchor="center")
    entry_estado = tk.Entry(root)
    entry_estado.place(relx=0.5, rely=0.4, anchor="center")

    label_cpf = tk.Label(root, text="CPF")
    label_cpf.place(relx=0.3, rely=0.5, anchor="center")
    entry_cpf = tk.Entry(root)
    entry_cpf.place(relx=0.5, rely=0.5, anchor="center")

    label_curso = tk.Label(root, text="Curso")
    label_curso.place(relx=0.3, rely=0.6, anchor="center")
    entry_curso = tk.Entry(root)
    entry_curso.place(relx=0.5, rely=0.6, anchor="center")

    # Botões
    button_salvar = tk.Button(root, text="Salvar", command=salvar_dados, bg="blue", fg="white")
    button_salvar.place(relx=0.5, rely=0.7, anchor="center")

    button_mostrar = tk.Button(root, text="Mostrar Dados", bg="pink" , command=mostrar_dados)
    button_mostrar.place(relx=0.5, rely=0.8, anchor="center")

    button_quit = tk.Button(root, text="Quit", command=root.destroy)
    button_quit.place(relx=0.5, rely=0.9, anchor="center")

    root.mainloop()

Main()