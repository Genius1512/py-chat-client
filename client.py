from networking import Client
from threading import Thread


class App:
    def __init__(self):
        self.client = Client()
        self.client.setup(port=1512)

        self.client.post(input("Name: "))

        t = Thread(target=self.get_messages, daemon=True)
        t.start()

        done = False
        while not done:
            message = input("")

            if message == ".exit":
                done = True
                self.client.post(".exit")
            else:
                self.client.post(message)


    def get_messages(self):
        while True:
            message = self.client.get() + "\n"
            print(message)


if __name__ == "__main__":
    app = App()