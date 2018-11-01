
import argparse
import socket
import time


class TaskQueueServer:

	def __init__(self, ip, port, path, timeout):
		self.ip = ip
		self.port = port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


	def run(self):
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind((self.ip, self.port))
		print(f'server is running on {self.ip} on port {self.port}')
		self.s.listen()
		self.__main()

	def close(self):
		pass

	def terminate(self):
		self.s.close()

	def wait(self, secs):
		time.sleep(secs)

	def __main(self):
		while True:
			conn, addr = self.s.accept()
			handle = ConnectionHandler(conn)
			handle.work()
			self.wait(300)


class ConnectionHandler:
	def __init__(self, conn):
		self.conn = conn
		self.commands = Commands()


	def work(self):
		print(f'You are here! {self.conn}')
		# waiting for message
		recv = self.conn.recv(1024).split()
		if self.commands.parse(recv) is None:
			self.conn.close()





class Commands:
	def __init__(self):
		self.commands = ['GET', 'ADD', 'ACK', 'IN', 'SAVE']

	def parse(self, recv):
		if recv[0].decode() not in self.commands:
			return
		else:
			pass


	def _add(self):
		pass

	def _get(self):
		pass

	def _ack(self):
		pass

	def _in(self):
		pass

	def _save(self):
		pass


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
