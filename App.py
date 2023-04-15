import tkinter 
import customtkinter as ctk
from tkinter import *
import sqlite3
from tkinter import messagebox
import re
import bcrypt


class BackEnd():
    def conecta_db(self):
        self.conn = sqlite3.connect("Testes.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados conectado")

    def desconecta_db(self):
        self.conn.close()
        print("Banco de dados desconectado")

    def cria_tabela(self):
        self.conecta_db()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT, 
                Username TEXT NOT NULL UNIQUE,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_Senha TEXT NOT NULL
            );
        """)
        self.conn.commit()
        print("Tabela criado com sucesso")
        self.desconecta_db()


    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha = self.confirma_senha_entry.get()

        
        
        print(self.senha_cadastro)

        print(self.username_cadastro)

        self.conecta_db()


        self.cursor.execute(""" 
            INSERT INTO Usuarios (Username, Email, Senha, Confirma_Senha)
            VALUES (?, ?, ?, ?)""", (self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirma_senha))
         
        self.cursor.execute(""" SELECT * FROM Usuarios WHERE (Username = ?) """,[self.username_cadastro]) 
        self.verifica_consulta = self.cursor.fetchall()
        print(self.verifica_consulta)


        #restrições
        try:
            if (self.username_cadastro=="" or self.email_cadastro=="" or self.senha_cadastro=="" or self.confirma_senha==""):
                messagebox.showerror(title="Sistema de login", message="ERROR!!!\nPor favor, preencha todos os campos")

            elif not re.match(r"[^@]+@[^@]+\.[^@]+", self.email_cadastro):
                messagebox.showwarning(title="Sistema de Login", message="Email inválido")

            elif(len(self.verifica_consulta)>=2):
                messagebox.showerror(title="Sistema de login", message="ERROR!!!\nUSUARIO CADASTRADO")
            

            elif(len(self.username_cadastro)<=4 ): #procurar outros formatos de leitura em python para definir os metodos de segurança
                messagebox.showwarning(title="Sistema de Login", message="O nome de usuario deve ser com no minimo 4 caracteres")
                    
            elif not re.match(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$.*&@#])[0-9a-zA-Z$*&.@#]{6,}$", self.senha_cadastro): 
                messagebox.showwarning(title="Sistema de Login", message="A senha de usuario deve ter no minimo:\n6 caracteres\n1 caracter especial($*&.@#)\n1 Letra maiuscula")
                
            elif(self.confirma_senha != self.senha_cadastro):
                messagebox.showerror(title="Sistema de Login", message="ERROR!!!\nSenhas não coincidem")

            else: 
                self.conn.commit()
              

                print(self.verifica_consulta)
                messagebox.showinfo(title="Sistema de Login", message=f"Parabens, {self.username_cadastro}\nUsuario cadastrado com sucesso!")
                self.desconecta_db()
                self.limpa_entry_cadastro()
        except:
            messagebox.showerror(title="Sistema de Login", message="Error ao cadastrar\nTente novamente")
            self.desconecta_db()

    

    def verifica_login(self):
        self.username_login = self.username_login_entry.get()
        self.senha_login = self.senha_login_entry.get()
        #print(self.username_login, self.senha.login)
        #self.limpa_entry_login()

        self.conecta_db()
        #selecione dentro da tabela de usuarios onde o username é igual a fulano e a senha é igual a fulano
        self.cursor.execute("""SELECT * FROM Usuarios WHERE (Username = ? AND Senha = ?)""",
            (self.username_login, self.senha_login)) 
        
        self.verifica_dados = self.cursor.fetchone() #percorrendo na tabela usuarios
        print("teste 1",self.verifica_dados)

        try:
            if(self.username_login =="" or self.senha_login ==""):
                messagebox.showwarning(title="Sistema de Login", message="Preencha todos os campos")

            elif(self.username_login in self.verifica_dados and self.senha_login in self.verifica_dados):
                messagebox.showinfo(title="Sistema de Login", message=f"Parabens {self.username_login}\nLogin feito com sucesso")
                print("teste 2",self.verifica_dados)
                self.desconecta_db()
                self.limpa_entry_login()
        except:
            messagebox.showerror(title="Sistema de Login", message="ERROR!!!\nDados não encontrados, verifique o login ou se cadastre no sistema")
            self.desconecta_db()



class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracao_da_janela_inicial()
        self.tela_de_login()
        self.cria_tabela()

#configurando a janela principal
    def configuracao_da_janela_inicial(self):
        self.geometry("700x400")
        self.title("Sistema de Login")
        self.resizable(False, False)

    def tela_de_login(self):
        #trabalhando com as imagens
        self.img = PhotoImage(file="Mobile encryption-bro.png")
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=10)

        #Titulo da nossa plataforma
        self.title = ctk.CTkLabel(self, text="Faça seu login ou Cadastre-se\nna nossa plataforma para acessar\nos nossos serviços", font=("Century Gothic bold", 14))
        self.title.grid(row=0, column=0, pady=10, padx=10)
        self.title.place(x=10, y=10)

        #criar o frame do formulario de login
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=350, y=10)

        #colocando widgets dentro do frame - formulario de login
        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça seu login",font=("Century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Seu nome de usuario", font=("Century Gothic bold", 16),corner_radius=16, border_color="blue")
        self.username_login_entry.grid(row=1, column=0, padx=10, pady=10)

        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Senha", font=("Century Gothic bold", 16), corner_radius=15, border_color="blue", show="*")
        self.senha_login_entry.grid(row=2, column=0, padx=10, pady=10)

        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text="Clique para ver a senha", font=("Century Gothic bold", 12), corner_radius=20)
        self.ver_senha.grid(row=3, column=0, padx=10, pady=10)

        self.btn_login = ctk.CTkButton(self.frame_login, width=300, text="Fazer Login", font=("Century Gothic bold", 16), corner_radius=15, command=self.verifica_login)
        self.btn_login.grid(row=4, column=0, padx=10, pady=10)

        self.span = ctk.CTkLabel(self.frame_login, text="Se não tem conta, clique no botao abaixo para se cadastrar", font=("century Gothic", 10))
        self.span.grid(row=5, column=0, pady=10, padx=10)

        self.btn_cadastro= ctk.CTkButton(self.frame_login, width=300, fg_color="green", hover_color="#050", text="Fazer Cadastro",
        font=("Century Gothic bold", 16), corner_radius=15, command=self.tela_de_cadastro)
        self.btn_cadastro.grid(row=6, column=0, padx=10, pady=10)


    def tela_de_cadastro(self):
        #Remover o folumario de login
        self.frame_login.place_forget() 

        #frame de cadastro
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=350, y=10)

        #criando o nosso titulo 
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Faça seu login",font=("Century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=5)


        #criar nossos widgets de cadastro
        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Seu nome de usuario", font=("Century Gothic bold", 16),corner_radius=16, border_color="blue")
        self.username_cadastro_entry.grid(row=1, column=0, padx=10, pady=5)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Seu email de usuario", font=("Century Gothic bold", 16),corner_radius=16, border_color="blue")
        self.email_cadastro_entry.grid(row=2, column=0, padx=10, pady=5)

        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Senha de usuario", font=("Century Gothic bold", 16), corner_radius=15, border_color="blue", show="*")
        self.senha_cadastro_entry.grid(row=3, column=0, padx=10, pady=5)

        self.confirma_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="confirma senha de usuario.", font=("Century Gothic bold", 16)
        ,corner_radius=16, border_color="blue", show="*")
        self.confirma_senha_entry.grid(row=4, column=0, padx=10, pady=5)

        self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, text="Clique para ver a senha", font=("Century Gothic bold", 12), corner_radius=20)
        self.ver_senha.grid(row=5, column=0, pady=5)

        self.btn_cadastrar_user= ctk.CTkButton(self.frame_cadastro, width=300, fg_color="green", hover_color="#050", text="Fazer Cadastro",
        font=("Century Gothic bold", 16), corner_radius=15, command=self.cadastrar_usuario)
        self.btn_cadastrar_user.grid(row=6, column=0, padx=10, pady=5)

        
        self.btn_login_back= ctk.CTkButton(self.frame_cadastro, width=300, text="Voltar a Login", font=("Century Gothic bold", 16),
        corner_radius=15, fg_color="#444", hover_color="#333", command=self.tela_de_login)
        self.btn_login_back.grid(row=7, column=0, padx=10, pady=5)


    def limpa_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirma_senha_entry.delete(0, END)
        
    def limpa_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)
#pra limpar a imagem teria que adicionar aqui tbm



if __name__=="__main__": # os elementos resetados aqui são desse modo
    app = App()
    app.mainloop()