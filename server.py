from networking import Server
from threading import Thread


class App:
    def __init__(self):
        self.server = Server()

        self.server.setup(port=1512)

        self.threads = []
        for id in range(1, 10):
            t = Thread(target=self.new_connection, args=(str(id),))
            self.threads.append(t)
            self.threads[-1].start()

    def new_connection(self, id):
        self.server.new_connection(id)

        name = self.server.get(id)

        done = False
        while not done:
            message = self.server.get(id)
            if message == ".exit":
                done = True
            else:
                message = f'{name}: {message}'
                for connection in self.server.connections:
                    self.server.post([connection], message)


if __name__ == "__main__":
    server = App()