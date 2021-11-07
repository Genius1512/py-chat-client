from high_lvl_networking import Client
from socket import gethostname, gethostbyname
from sys import argv


class App:
    def __init__(self, ip, port):
        self.client = Client()
        self.client.setup(ip=ip, port=port)

        self.client.post(input("Name: "))

        done = False
        while not done:
            message = self.get_message()

            if message == ".exit":
                done = True
                self.client.post(".exit")
            else:
                self.client.post(message)

    def get_message(self):
        done = False
        message = ""

        while not done:
            line = input("")
            if line == ".":
                done = True
            else:
                message += "\n" + line

        print("Sent\n")
        return message


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

    app = App(ip, port)