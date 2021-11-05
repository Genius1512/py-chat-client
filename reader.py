from socket import *
from networking import Client
from rich import print


class App:
	def __init__(self):
		self.client = Client()
		self.client.setup(port=1512)

		self.client.post("reader")

		while True:
			message = self.client.get()
			self.print_message(message)

	def print_message(self, message):
		message = message.split(": ", 1)

		print(f'[blue]{message[0]}[/blue]: {message[1]}')


if __name__ == "__main__":
	app = App()
