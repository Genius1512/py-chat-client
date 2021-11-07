from socket import gethostname, gethostbyname
from high_lvl_networking import Client
from rich import print
from sys import argv


class App:
	def __init__(self, ip, port):
		self.client = Client(debug=False)
		self.client.setup(ip=ip, port=port)

		self.client.post("reader")

		while True:
			message = self.client.get()
			self.print_message(message)

	def print_message(self, message):
		message = message.split(": ", 1)

		print(f'[blue]{message[0]}[/blue]: {message[1]}\n')


if __name__ == "__main__":
	ip = None
	port = None

	try:
		if argv[1] == "debug":
			ip = gethostbyname(gethostname())
			port = 1512
		else:
			ip = input("IP: ")
			port = int(input("Port: "))
	except IndexError:
		ip = input("IP: ")
		port = int(input("Port: "))

	app = App(ip=ip, port=port)
