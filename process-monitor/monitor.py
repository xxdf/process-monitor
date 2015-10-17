from time import sleep
from tkinter import *
from tkinter import messagebox
from threading import Thread
import threading
import platform
import subprocess
import tasklist_process as tp
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
		self.monitorando = False
		self.pack() # Topo (Padrão)
		self.createWidgets()
	def monitoraThread(self, serv):
		print("Monitorando")
		while True:
			if self.monitorando == True:
				tp.monitora()
				sleep(5)
			else:
				break
	def ProcessRun(self):
		if not self.monitorando:
			self.btListaProcessos.config(fg = "white", bg = "blue")
			self.th=Thread(target=self.monitoraThread, args = (self,))
			self.th.start()
			self.btListaProcessos.config(text="Monitorando...")
			self.monitorando = True
		else:
			self.btListaProcessos.destroy()
			self.btListaProcessos = Button(self, text="Monitorar", width=13,
				height=1, command=self.ProcessRun)#.pack({'side':'left'})
			self.btListaProcessos.pack({'side':'left'})
			self.monitorando = False
	def editaTabela(self):
		if self.monitorando:
			messagebox.showinfo("ATENÇÃO","Pare de monitorar para acessar o BD..")
		else:
			self.janela=Toplevel()
			self.janela.title("Lista de Excessão")
			Label(self.janela, text="Processos (Lista de Excessão)", width=46,
				height=3, font=("Arial", '12', 'bold')).grid(columnspan=2)
			btListar = Button(self.janela, text="LISTAR")
			btListar['width'] = 8
			btListar['height']= 1
			btListar['command'] = self.imprime
			btListar.grid(columnspan=2, row=2)
			btRemover = Button(self.janela, text="REMOVER")
			btRemover['command'] = self.deletar
			btRemover['width'] = 8
			btRemover['height']= 1
			btRemover.grid(columnspan=2, row=3)
			self.txtPid = Entry(self.janela, width=10)
			self.txtPid.focus_force()
			self.txtPid.grid(columnspan=2, row=4)
			Label(self.janela, text="    PID", font='Papyrus', width=4,
				height=3).grid(column=0, row=4)
			btSair = Button(self.janela, text="SAIR", command=self.fecha_janela
			,bg="red", fg="white")
			btSair['width'] = 8
			btSair['height']= 1
			btSair.grid(columnspan=2)
			self.janela.geometry('500x400')
			self.janela.maxsize(500, 400)
			self.janela.minsize(500, 400)
			self.janela.transient(root)#
			self.janela.focus_force()#
			self.janela.grab_set()#
	def imprime(self):
		self.tela = Tk()
		self.tela.title("Processos em banco")
		scr = Scrollbar(self.tela)
		scr.pack(side=RIGHT, fill=Y)
		self.tela.geometry('500x400')
		self.tela.maxsize(500, 400)
		self.tela.minsize(500, 400)
		Label(self.tela, text="LISTA DE\nEXCESSÕES", font=('Papyrus','14')).pack()
		listbox = Listbox(self.tela, yscrollcommand=scr.set, font=("Papyrus", '10'))
		listbox.insert(END, "%s %s" %("Processos".center(80),"PID".center(5)))
		tabela, qtd = tp.imprProcessos()
		for i, tb in enumerate(tabela):
			listbox.insert(END,"%s (%05d)"%(tb[0].ljust(80),tb[1]))
		listbox.pack(side=LEFT, fill=BOTH, expand=1)
		scr.config(command=listbox.yview)
	def deletar(self):
		# VERIFICAR SE O CONTEÚDO É DO TIPO INTEIRO...
		# VERIFICAR (CRIAR FUNÇÃO) SE O PID ESTA NO BANCO ANTES DE DELETAR
		pid = self.txtPid.get()
		pid = str(pid).strip()
		if pid == None or not pid:
			messagebox.showinfo("O campo não pode ser Nulo",
				'''Preencha o campo com o 'PID' que deseja remover da lista''')
			sleep(0.2)
		else:
			pid = int(pid)
			tp.deleta(pid)
			sleep(0.2)
	def fecha_janela(self):
		self.janela.destroy()
	def createWidgets(self):
		self.lbPrincipal = Label(self, text="Menu Principal", width=46, height=3,
			font=("Arial", '12', 'bold'))
		self.lbPrincipal.pack(expand = 1)
		self.QUIT = Button(self)
		self.QUIT["text"] = "SAIR"
		self.QUIT["fg"] = "white"
		self.QUIT["bg"] = "red"
		self.QUIT['width'] = 13
		self.QUIT['height']= 1
		self.QUIT["command"] = self.quit
		self.QUIT.pack({"side": "left"})
		self.btListaExcessao = Button(self)
		self.btListaExcessao["text"] = "Editar Tabela"
		self.btListaExcessao['width'] = 13
		self.btListaExcessao['height']= 1
		self.btListaExcessao["command"] = self.editaTabela
		self.btListaExcessao.pack({"side": "left"})
		self.btListaProcessos = Button(self)
		self.btListaProcessos["text"] = "Monitorar"
		self.btListaProcessos['width'] = 13
		self.btListaProcessos['height']= 1
		self.btListaProcessos["command"] = self.ProcessRun
		self.btListaProcessos.pack({'side':'left'})
# main
root = Tk()
app = Application(master=root)
app.master.title('Menu')
app.master.maxsize(300, 200)
app.master.minsize(300, 200)
root.geometry('300x200')
app.mainloop()
