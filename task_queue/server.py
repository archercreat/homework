
import argparse
import socket
import time
import json
import sys


class TaskQueueServer:

	def __init__(self, ip, port, path, timeout):
		self.ip = ip
		self.port = port
		self.path = path
		self.timeout = timeout
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.buffer = 4096


	def recvall(self, conn):
		data = b''
		while True:
			buff = conn.recv(self.buffer)
			data += buff
			if len(buff) < self.buffer:
				break
		return data


	def save(self):
		return 'OK\n'


	def run(self):
		try:
			self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.sock.bind((self.ip, self.port))
			print(f'server is running on {self.ip} on port {self.port}')
			self.sock.listen()
			self.main()
		except KeyboardInterrupt:
			print('\nclosing server')
			self.sock.close()
			sys.exit(0)

	def main(self):
		while True:
			conn, addr = self.sock.accept()
			data = self.recvall(conn).decode().rstrip().split()
			if data[0] == 'SAVE':
				conn.send(self.save().encode())
			conn.close()


class ConnectionHandler:
	def __init__(self, conn):
		self.conn = conn
		self.commands = Commands()


	def work(self):
		# print(f'You are here! {self.conn}')
		# waiting for message
		recv = self.conn.recv(1024).split()
		if self.commands.parse(recv) is None:
			self.conn.close()


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


