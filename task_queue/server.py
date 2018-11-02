
import argparse
import socket
import time
import json
from datetime import datetime
import sys
import os
import pickle
from collections import OrderedDict
from uuid import uuid1


class Task:
	def __init__(self, length, data):
		self.length = length
		self.data = data
		self.id = uuid1().hex
		self.time = 0

	def __repr__(self):
		return f'id ({self.id}), time ({self.time})'

	def is_in_work(self, current_time, timeout):
		return current_time - self.time < timeout

	def set_time(self):
		self.time = int(datetime.now().timestamp())




class TaskQueueServer:
	filename = 'log'

	def __init__(self, ip, port, path, timeout):
		self.ip = ip
		self.port = port
		self.path = path
		self.timeout = timeout
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.buffer = 4096
		self.filepath = os.path.join(self.path, self.filename)
		self.commands = {
			'ADD':	self.add_command,
			'GET':	self.get_command,
			'ACK':	self.ack_command,
			'IN':	self.in_command,
			'SAVE':	self.save_command,
		}
		self.current_time = 0
		self.LIST_OF_QUEUES = self.load()


	def load(self):
		return {}


	def recvall(self, conn):
		data = b''
		while True:
			buf = conn.recv(self.buffer)
			data += buf
			if len(buf) < self.buffer:
				break
		return data


	def save(self):
		return 'OK\n'


	def run(self):
		try:
			self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.sock.bind((self.ip, self.port))
			self.sock.listen()
			print(f'server is running on {self.ip} on port {self.port}')
			self.main()

		except KeyboardInterrupt:
			print('\nclosing server..')
			self.sock.close()
			sys.exit(0)


	def main(self):
		while True:
			conn, addr = self.sock.accept()
			data = self.recvall(conn).decode().rstrip().split()
			if data[0] == 'SAVE':
				conn.send(self.save().encode())
			else:
				handle = ConnectionHandler(conn)
				handle.operate()
			conn.close()

'''
class ConnectionHandler:
	def __init__(self, conn):
		self.conn = conn
		self.commands = Commands()
		# self.LIST_OF_QUEUES


	def operate(self):
		# print(f'You are here! {self.conn}')
		# waiting for message
		recv = self.conn.recv(1024).split()
		if self.commands.parse(recv) is None:
			self.conn.close()


	def add_cmd(self, user_input):
		in not user_input or len(user_input) != 3:
			return
		try:
			str(queue_name), int(length), str(data) = user_input
		except ValueError:
			return
		if length > 10**6 or length != len(data):
			return


	def in_cmd(self, user_input):
		if not user_input or len(user_input) != 2:
			return
		queue_name, task_id = user_input
		queue = self.LIST_OF_QUEUES.get(queue_name)
		if not queue:
			return

		for task in queue['tasks']:
			if task['id'] == task_id:
				return b'YES'
		return b'NO'

	def get_cmd(self, user_input):
		if not user_input or len(user_input) != 1:
			return
		queue_name = user_input
		queue = self.LIST_OF_QUEUES.get(queue_name)
		if not queue:
			return 'NONE'
		return queue		

	def ack_cmd(self, user_input):
		if not user_input or len(user_input) != 2:
			return
		queue_name, task_id = user_input
		queue = self.LIST_OF_QUEUES.get(queue_name)
		if not queue:
			return
		for task in queue['tasks']:
			if task['id'] == task_id:
				return 'YES'
		return 'NO'
'''



def parse_args():
	parser = argparse.ArgumentParser(description='This is a simple task queue server with custom protocol')
	parser.add_argument(
		'-p',
		action="store",
		dest="port",
		type=int,
		default=5555,
		help='Server port')
	parser.add_argument(
		'-i',
		action="store",
		dest="ip",
		type=str,
		default='0.0.0.0',
		help='Server ip adress')
	parser.add_argument(
		'-c',
		action="store",
		dest="path",
		type=str,
		default='./',
		help='Server checkpoints dir')
	parser.add_argument(
		'-t',
		action="store",
		dest="timeout",
		type=int,
		default=300,
		help='Task maximum GET timeout in seconds')
	return parser.parse_args()

if __name__ == '__main__':
	args = parse_args()
	server = TaskQueueServer(**args.__dict__)
	server.run()

	# data = {"queue": "lol", "len": "6", "data": "123456"}


