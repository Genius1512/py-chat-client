# The server for my chat client

# imports
from high_lvl_networking import Server
from threading import Thread
from sys import argv
from tkinter import *


# Main App
class App:
    def __init__(self, port: int, listen_to: int = 50):
        # setup server
        self.server: Server = Server(debug=False)
        self.server.setup(port=port, listen_to=listen_to*2)

        # names that are not allowed
        self.invalid_names: list[str] = ["[server]"] 

        # status and names are stored in this
        self.connections: dict[str, str] = {}


        # init Tk
        self.gui: Tk = Tk("Server GUI") # create
        self.gui.geometry("820x660") # dimensions
        self.gui.configure(bg="#1e1e1e") # colors
        self.gui.resizable(False, False) # make not resizable
        self.gui.title("Server") # set title


        # add widgets
        self.server_log: Text = Text(self.gui)
        self.server_log.grid(row=0, column=0, sticky="NSEW")
        self.server_log.place(
            x=10,
            y=10,
            width=400,
            height=600
        )
        # readonly
        self.server_log.bind("<Key>", lambda e: "break")
        self.server_log.configure(bg="#252527",
            fg="#9cdcfe",
            font=('Helvatical bold', 14),
            insertbackground="#9cdcfe"
        )


        self.server_information_text: Text = Text(self.gui)
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


        self.quit_button: Button = Button(command=quit, text="Quit")
        self.quit_button.grid(row=1, column=1, sticky="NSEW")
        self.quit_button.place(
            x=380,
            y=620,
            width=60,
            height=30
        )
        self.quit_button.configure(bg="#007acc", fg="#000000")


        # create threads
        self.threads: list[Thread] = []
        for id in range(1, listen_to*2):
            t: Thread = Thread(target=self.new_connection, args=(str(id),))
            self.threads.append(t)
            self.threads[-1].start()

        print("Server setup")

        # start gui
        self.gui.mainloop()

    # add new connections
    def new_connection(self, id: str):
        # networking lvl connection adding
        self.server.new_connection(id)

        # get name
        name: str = self.server.get(id)
        if name == "client":
            name = "Client" + id

        self.log(f"New connection: '{name}'")


        # inform every client for the new connection
        for connection in self.server.connections:
            try:
                self.server.post([connection], f'[Server]: {name} connected')
            except Exception:
                pass

        done: bool = False

        if name.lower() in self.invalid_names + list(self.connections.keys()):
            self.log(f"'{name}' had an invalid name")
            self.server.post([id], "Invalid name")
            done = True

        # update server information
        if not done:
            self.connections[name] = {"status": "on"}
            self.update_server_information()
        
        while not done:
            # get message
            try:
                message: str = self.server.get(id)
                self.log(f'{name} sent message: {message}')
            except Exception:
                done: bool = True
                break
            
            # on disconnect
            if message == ".exit":
                done: bool = True
                break
            # forward message
            else:
                message = f'{name}: {message}'
                message = message.replace("\n", f"\n{' '*(len(name) + 7)}")
                for connection in self.server.connections:
                    try:
                        self.server.post([connection], message)
                    except Exception:
                        pass
        
        # on disconnect
        for connection in self.server.connections:
            try:
                self.server.post([connection], f'[Server]: {name} disconnected')
            except Exception:
                pass
        
        self.log(f"'{name}' disconnected")

        self.connections[name]["status"] = "off"
        self.update_server_information()

    # log messages
    def log(self, message: str):
        self.server_log.insert(END, message + "\n")
        self.server_log.see(END)

    # update server information
    def update_server_information(self):
        # clear information field
        self.server_information_text.delete("1.0", END)

        # add informations
        for name in self.connections:
            inf = f'{name}: {self.connections[name]["status"]}\n'
            self.server_information_text.insert(END, inf)
        # scroll to end
        self.server_information_text.see(END)


if __name__ == "__main__":
    # get setup information
    port = None
    try:
        if argv[1] == "debug":
            port = 1512
        else:
            port = int(input("Port: "))
    except IndexError:
        port = int(input("Port: "))

    server = App(port=port)