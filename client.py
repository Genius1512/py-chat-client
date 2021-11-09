# imports
from high_lvl_networking import Client
from socket import gethostname, gethostbyname
from sys import argv
from tkinter import *
from keyboard import add_hotkey
from threading import Thread


# Main App
class App:
    def __init__(self, ip: str, port: int, name: str = None) -> None:
        # setup networking
        self.client: Client = Client(debug=False)
        self.client.setup(ip=ip, port=port)

        # get name
        if name == None:
            name = input("Name: ")
        else:
            name = name
        self.client.post(name)


        # init gui
        self.gui: Tk = Tk("Chat Client GUI")
        self.gui.geometry("820x660")
        self.gui.configure(bg="#1e1e1e")
        self.gui.resizable(False, False)
        self.gui.protocol("WM_DELETE_WINDOW", self.on_close)
        self.gui.title(name)
        
        # fast sending
        add_hotkey("ctrl + enter", self.send)


        # input field
        self.entry_field: Text = Text(self.gui)
        self.entry_field.grid(row=0, column=0, sticky="NSEW")
        self.entry_field.place(
            x=10,
            y=10,
            width=400,
            height=600
        )
        self.entry_field.configure(bg="#252527",
            fg="#9cdcfe",
            font=('Helvatical bold', 14),
            insertbackground="#9cdcfe"
        )


        # chat
        self.chat_text: Text = Text(self.gui)
        self.chat_text.grid(row=0, column=1, sticky="NSEW")
        self.chat_text.place(
            x=410,
            y=10,
            width=400,
            height=600
        )
        self.chat_text.bind("<Key>", lambda e: "break")
        self.chat_text.configure(
            bg="#252527",
            fg="#9cdcfe",
            font=('Helvatical bold',14)
        )


        # button to send
        self.send_button: Button = Button(command=self.send, text="Send")
        self.send_button.grid(row=1, column=1, sticky="NSEW")
        self.send_button.place(
            x=380,
            y=620,
            width=60,
            height=30
        )
        self.send_button.configure(
            bg="#007acc",
            fg="#000000",
        )


        # button to quit
        self.quit_button: Button = Button(command=self.on_close, text="Quit")
        self.quit_button.grid(row=1, column=1, sticky="NSEW")
        self.quit_button.place(
            x=580,
            y=620,
            width=60,
            height=30
        )
        self.quit_button.configure(bg="#007acc", fg="#000000")


        # setup threads
        recveiver: Thread = Thread(target=self.get_messages, daemon=True)
        recveiver.start()


        # start gui
        self.gui.mainloop()

    # send messages
    def send(self):
        # remove last enter
        message = self.entry_field.get("1.0", END)[::-1]
        message = message.replace("\n", "", 1)
        message = message[::-1]
        if not message == "":
            self.client.post(message)
        self.entry_field.delete("1.0", END) 

    # recveive messages
    def get_messages(self):
        while True:
            message = self.client.get()
            if message == "Invalid name":
                quit()
            self.print_message(message)

    # log messages to chat
    def print_message(self, message):
        self.chat_text.insert(END, message + "\n")
        self.chat_text.see(END)

    # activate on close; destory gui and disconnect
    def on_close(self):
        self.client.post(".exit")
        self.gui.destroy()
        quit()


# start main
if __name__ == "__main__":
    ip = None
    port = None
    name = None
    
    # get information
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

    # init app
    app = App(ip, port, name=name)
