from high_lvl_networking import Client


class App:
    def __init__(self):
        self.client = Client()
        self.client.setup(port=1512)

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
    app = App()