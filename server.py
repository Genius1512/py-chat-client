from high_lvl_networking import Server
from threading import Thread
from sys import argv
from tkinter import *


class App:
    def __init__(self, port, listen_to=50):
        self.server = Server(debug=False)
        self.server.setup(port=port, listen_to=listen_to*2)

        self.invalid_names = ["[server]"]

        self.connections = {}


        self.gui = Tk("Server GUI")
        self.gui.geometry("820x660")
        self.gui.configure(bg="#1e1e1e")
        self.gui.resizable(False, False)
        self.gui.title("Server")


        self.server_log = Text(self.gui)
        self.server_log.grid(row=0, column=0, sticky="NSEW")
        self.server_log.place(
            x=10,
            y=10,
            width=400,
            height=600
        )
        self.server_log.bind("<Key>", lambda e: "break")
        self.server_log.configure(bg="#252527",
            fg="#9cdcfe",
            font=('Helvatical bold', 14),
            insertbackground="#9cdcfe"
        )


        self.server_information_text = Text(self.gui)
        self.server_information_text.grid(row=0, column=1, sticky="NSEW")
        self.server_information_text.place(
            x=410,
            y=10,
            width=400,
            height=600
        )
        self.server_information_text.bind("<Key>", lambda e: "break")
        self.server_information_text.configure(
            bg="#252527",
            fg="#9cdcfe",
            font=('Helvatical bold',14)
        )


        self.quit_button = Button(command=quit, text="Quit")
        self.quit_button.grid(row=1, column=1, sticky="NSEW")
        self.quit_button.place(
            x=380,
            y=620,
            width=60,
            height=30
        )
        self.quit_button.configure(bg="#007acc", fg="#000000")


        self.threads = []
        for id in range(1, listen_to*2):
            t = Thread(target=self.new_connection, args=(str(id),))
            self.threads.append(t)
            self.threads[-1].start()

        print("Server setup")

        self.gui.mainloop()

    def new_connection(self, id):
        self.server.new_connection(id)

        name = self.server.get(id)
        if name == "client":
            name = "Client" + id

        self.log(f"New connection: '{name}'")


        for connection in self.server.connections:
            try:
                self.server.post([connection], f'[Server]: {name} connected')
            except Exception:
                pass

        done = False

        if name.lower() in self.invalid_names:
            self.log(f"'{name}' had an invalid name")
            self.server.post([id], "Invalid name")
            done = True

        if not done:
            self.connections[name] = {"status": "on"}
            self.update_server_information()
        
        while not done:
            try:
                message = self.server.get(id)
                self.log(f'{name} sent message: {message}')
            except Exception:
                done = True
                break
            if message == ".exit":
                done = True
                break
            else:
                message = f'{name}: {message}'
                message = message.replace("\n", f"\n{' '*(len(name) + 7)}")
                for connection in self.server.connections:
                    try:
                        self.server.post([connection], message)
                    except Exception:
                        pass

        for connection in self.server.connections:
            try:
                self.server.post([connection], f'[Server]: {name} disconnected')
            except Exception:
                pass
        
        self.log(f"'{name}' disconnected")

        self.connections[name]["status"] = "off"
        self.update_server_information()

    def log(self, message):
        self.server_log.insert(END, message + "\n")
        self.server_log.see(END)

    def update_server_information(self):
        self.server_information_text.delete("1.0", END)

        for name in self.connections:
            inf = f'{name}: {self.connections[name]["status"]}\n'
            self.server_information_text.insert(END, inf)
        self.server_information_text.see(END)


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