from high_lvl_networking import Server
from threading import Thread
from sys import argv


class App:
    def __init__(self, port, listen_to=50):
        self.server = Server(debug=True)

        self.server.setup(port=port, listen_to=listen_to*2)

        self.threads = []
        for id in range(1, listen_to*2):
            t = Thread(target=self.new_connection, args=(str(id),))
            self.threads.append(t)
            self.threads[-1].start()

    def new_connection(self, id):
        self.server.new_connection(id)

        name = self.server.get(id)
        if name == "client":
            name = "Client" + id

        for connection in self.server.connections:
            try:
                self.server.post([connection], f'[Server]: {name} connected')
            except Exception:
                pass

        done = False
        while not done:
            try:
                message = self.server.get(id)
            except Exception:
                done = True
                break
            print("Recveived message")
            if message == ".exit":
                done = True
            else:
                message = f'{name}: {message}'
                for connection in self.server.connections:
                    try:
                        self.server.post([connection], message)
                    except Exception:
                        pass


if __name__ == "__main__":
    port = None
    try:
        if argv[1] == "debug":
            port = 1512
        else:
            port = int(input("Port: "))
    except IndexError:
        port = int(input("Port: "))

    server = App(port=port)