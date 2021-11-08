from high_lvl_networking import Client
from socket import gethostname, gethostbyname
from sys import argv
from tkinter import *
from keyboard import add_hotkey
from threading import Thread


class App:
    def __init__(self, ip, port, name=None):
        self.client = Client(debug=False)
        self.client.setup(ip=ip, port=port)

        self.gui = Tk("Chat Client GUI")
        self.gui.geometry("820x260")
        self.gui.configure(bg="#1e1e1e")
        self.gui.resizable(False, False)

        add_hotkey("ctrl + enter", self.send)

        if name == None:
            self.client.post(input("Name: "))
        else:
            self.client.post(name)

        self.gui.title(name)

        self.entry_field = Text(self.gui)
        self.entry_field.grid(row=0, column=0, sticky="NSEW")
        self.entry_field.place(
            x=10,
            y=10,
            width=400,
            height=200
        )
        self.entry_field.configure(bg="#252527",
            fg="#9cdcfe",
            font=('Helvatical bold', 14),
            insertbackground="#9cdcfe"
        )

        self.chat_text = Text(self.gui)
        self.chat_text.grid(row=0, column=1, sticky="NSEW")
        self.chat_text.place(
            x=410,
            y=10,
            width=400,
            height=200
        )
        self.chat_text.bind("<Key>", lambda e: "break")
        self.chat_text.configure(bg="#252527", fg="#9cdcfe", font=('Helvatical bold',14))

        self.send_button = Button(command=self.send, text="Send")
        self.send_button.grid(row=1, column=1, sticky="NSEW")
        self.send_button.place(x=180,
            y=220,
            width=60,
            height=30
        )
        self.send_button.configure(bg="#007acc", fg="#000000")

        self.gui.grid_columnconfigure(0, weight=1)
        self.gui.grid_columnconfigure(1, weight=1)
        self.gui.grid_rowconfigure(0, weight=1)
        self.gui.grid_rowconfigure(1, weight=1)

        recveiver = Thread(target=self.get_messages, daemon=True)
        recveiver.start()

        self.gui.mainloop()

    def send(self):
        self.client.post(self.entry_field.get("1.0", END))

        self.entry_field.delete("1.0", END) 

    def get_messages(self):
        while True:
            print("Recvieving")
            message = self.client.get()
            print(message)
            self.print_message(message)

    def print_message(self, message):
	    self.chat_text.insert(END, message + "\n")


if __name__ == "__main__":
    ip = None
    port = None
    name = None

    try:
        if argv[1] == "debug":
            ip = gethostbyname(gethostname())
            port = 1512
            name = "client"
        else:
            ip = input("IP: ")
            port = int(input("Port: "))
    except IndexError:
        ip = input("IP: ")
        port = int(input("Port: "))

    app = App(ip, port, name=name)