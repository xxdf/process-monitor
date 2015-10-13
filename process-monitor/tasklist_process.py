import subprocess
from subprocess import *
import re
import sqlite3
from contextlib import closing
#-------------------- Funções --------------------------------
# Retorna os processos que estão atualmente rodando no Windows
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
# Cria tabelas para guardar os processos de 'excessão'
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
