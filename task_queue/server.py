
import argparse
import socket
import time
import json
from datetime import datetime
import sys
import os
import pickle
from collections import OrderedDict, deque
from uuid import uuid1


class Task:
	def __init__(self, length, data):
		self.length = length
		self.data = data
		self.id = uuid1().hex
		self.time = 0

	def __repr__(self):
		return f'id {self.id}, time {self.time}, length {self.length}'

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


# make load func
	def load(self):
		return {}




	def terminate(self, conn):
		conn.shutdown(1)
		conn.close()


	def recvall(self, conn):
		data = b''
		while True:
			buf = conn.recv(self.buffer)
			data += buf
			if len(buf) < self.buffer:
				break
		return data


# commands
	def save_command(self):
		return 'OK\n'

	def add_command(self, queue_name, length, data):
		queue = self.LIST_OF_QUEUES.get(queue_name)
		if not queue:
			self.LIST_OF_QUEUES[queue_name] = deque()
			queue = self.LIST_OF_QUEUES.get(queue_name)

		task = Task(length, data)
		queue.append(task)
		return f'task id {task.id}'


	def get_command(self, queue_name):
		# print(f'queue_name: {queue_name}, {type(queue_name)}')
		queue = self.LIST_OF_QUEUES.get(queue_name)
		# print(f'queue {queue}')
		if queue:
			for task in queue:
				print(task, task.is_in_work(self.current_time, self.timeout))
				if not task.is_in_work(self.current_time, self.timeout):
					task.set_time()
					return f'task id: {task.id}\nlength: {task.length}\ndata: {task.data}'
		return 'NONE\n'


	def in_command(self):
		return


	def ack_command(self):
		return


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
			answer = 'wrong commands'
			if not data:
				self.terminate(conn)

			command = data[0]
			function = self.commands.get(command)
			if function:
				try:
					answer = function(*data[1:])
				except TypeError:
					pass

			conn.sendall(answer.encode())
			print(self.LIST_OF_QUEUES)
			self.terminate(conn)


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


