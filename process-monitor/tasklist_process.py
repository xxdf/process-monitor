import subprocess
from subprocess import *
import re
import os
import sqlite3
from contextlib import closing
#-------------------- Funções --------------------------------
# Return the processes that is executing in Windows SO.
def get_processes_running():
	tasks = subprocess.check_output(['tasklist'])#.split("\r\n")
	tasks = str(tasks).split('\\r\\n')
	for i in range (3):
		del tasks[0]
	p = []
	for task in tasks:
		m = re.match("(.+?) +(\d+) (.+?) +(\d+) +(\d+.* K).*",task)
		if m is not None:
			p.append({"image":m.group(1),
				   "pid":m.group(2),
				   "session_name":m.group(3),
				   "session_num":m.group(4),
				   "mem_usage":m.group(5)
				   })
	print("get_processes_running.. OK")
	return p
# Create "processos's" table to put exception list
def criarTabela():
	print("criarTabela...")
	with sqlite3.connect("processos.db") as conexão:
		with closing(conexão.cursor()) as cursor:
			cursor.execute('''CREATE TABLE processos(
				id integer primary key autoincrement,
				image text,
				pid integer,
				sessionName text,
				sessionNum text,
				memUsage text)''')
		conexão.commit()
	print("\tTabela processos.. OK")
# Save obj 'p' on "processos's" table
def gravar(p):
	with sqlite3.connect("processos.db") as conexão:
		with closing(conexão.cursor()) as cursor:
			for x in p:
				cursor.execute('''INSERT into processos(
					image, pid, sessionName, sessionNum, memUsage)
				values(?, ?, ?, ?, ?)
					''',(x['image'], int(x['pid']),
						x['session_name'], x['session_num'],
						x['mem_usage']))
		conexão.commit()
	print("gravar..OK")
# Add the process on table 'processos', that's table of exceptions
def addExcessao(r):
	#r == process that will be added on base 'processos' to exception
	cursor.execute('''INSERT into processos(
		image, pid, sessionName, sessionNum, memUsage)
		values(?, ?, ?, ?, ?)''',(r['image'], int(r['pid']),
			r['session_name'], r['session_num'],
			r['mem_usage']))
	conexao.commit()
	messagebox.showinfo("Informação",
		"%s Adicionado á lista de excessoes.."%(r['image']))
# Print/returns data of processes from database (table 'processos')
def imprProcessos():
	count=0
	tabela = []
	with sqlite3.connect("processos.db") as conexão:
		with closing(conexão.cursor()) as cursor:
			print("%s %s"%("Nome do Processo".rjust(25),"PID".center(5)))
			print("="*78)
			query = ('SELECT image, pid from processos order by pid')
			for registro in cursor.execute(query):
				count +=1
				#image, pid = registro
				tabela.append(registro)
			print("imprProcessos..OK")
			return tabela, count
# Kill process that's not are on exception list and be authorized for user
def matarProcesso(pid, image):
	os.system("taskkill /f /IM %s"%(image))
	messagebox.showinfo("ÊXITO",
		"O processo [%s] foi morto!"%(image))
	print("matarProcesso..OK")
	# os.kill(int(pid),1)
# Remove from database (exception list) the process by PID (Integer)
def deleta(pid):
	i = True
	with sqlite3.connect("processos.db") as conexão:
		with closing(conexão.cursor()) as cursor:
			query = ('DELETE FROM processos WHERE pid = %d'%(pid))
			cursor.execute(query)
			if cursor.rowcount == 0:
				messagebox.showerror("Não encontrado",
					"PID informado não foi encontrado")
			else:
				#resposta = messagebox.showwarning("Deletar",
				if not messagebox.askokcancel("Deletar",
					"Deseja Deletar %d registros?"%(cursor.rowcount)):
					conexão.rollback()
					messagebox.showinfo("Falha","Operação Cancelada!")
				else:
					conexão.commit()
					messagebox.showinfo("Sucesso","Processo deletado!")
# monitor with a Thread
def monitora():
	print("Monitorando...") # Button
	rodando = get_processes_running()
	excessao = []
	temp = []
	with sqlite3.connect("processos.db") as conexão:
		with closing(conexão.cursor()) as cursor:
			query = ('SELECT image, pid FROM processos ORDER BY image')
			for registro in cursor.execute(query):
				excessao.append(registro)
			print("li o banco")
	for r in rodando:
		achou = False
		for e in excessao:
			if achou:
				break
			elif r['image'] == e[0]:
				achou = True
		if not achou:
			pode = True
			for t in temp:
				if r['image'] == t:
					pode = False
					break
			if pode:
				if messagebox.askquestion("ATENÇÃO",
					'''Novo processo encontrado [%s] (%05d)\nQuer adicioná-lo a lista de excessões e deixar executar?
					'''%(r["image"],int(r['pid']))) == 'yes':
					with sqlite3.connect("processos.db") as conexão:
						with closing(conexão.cursor()) as cursor:
							cursor.execute('''INSERT INTO processos(
								image, pid, sessionName, sessionNum, memUsage)
								VALUES(?, ?, ?, ?, ?)''',(r['image'], int(r['pid']),
									r['session_name'], r['session_num'],
									r['mem_usage']))
						conexão.commit()
						messagebox.showinfo("Informação",
							"%s Adicionado á lista de excessoes.."%(r['image']))
				else:
					# Mata processo e não adiciona em nada
					matarProcesso(int(r['pid']), r['image'])
					temp.append(r['image'])
#
