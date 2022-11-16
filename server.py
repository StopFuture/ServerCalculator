from socket import *
import logging


class Server:
    def __init__(self):
        user = None
        try:
            HOST = '192.168.1.38'
            PORT = 1025 + 9
            self.utf = 'utf-8'
            self.cnt = 0
            self.mx = -float("inf")
            self.mn = float("inf")
            self.sm = 0

            self.server = socket(
                AF_INET, SOCK_STREAM,
            )

            logging.getLogger("Server")
            logging.basicConfig(filename="server_log.log",
                                level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                filemode='a',
                                )

            logging.info("Server launched")

            self.try_connection(HOST, PORT)
            print(self.server.getblocking())

            user, addr = self.server.accept()

            print('Connected:', addr)
            logging.info(f'Connected to a client {addr}')
            user.send(self.start_msg().encode(self.utf))
            logging.info("Sent info")
            print('Listening...')
            logging.info('Listening to the client')

            try:
                while True:
                    data = user.recv(256).decode(self.utf)
                    logging.info(f'Received message: {data}')
                    print(f'Received message: {data}')
                    data = data[1:]

                    try:
                        ans = "=" + str(self.process_msg(data))
                        if not ans:
                            break
                        print(f"Send answer: {ans}")
                        if "stop" in ans:
                            ans += "\n" + self.final_msg()
                            user.send(ans.encode(self.utf))
                            logging.info(
                                f'Send answer: \n{ans}\n ')

                            logging.info("Stop marker founded.")
                            logging.info("Connection closed.")
                            break

                        user.send(ans.encode(self.utf))
                        logging.info(f'Sent answer: \n{ans}')

                    except Exception as exp:
                        print("Exception: ", exp)
                        break

            except Exception as exp:
                print("Error", exp)
                logging.info("Error. Connection closed.")
                user.send("stop".encode(self.utf))
        finally:
            try:
                user.close()
            except Exception as e:
                print(f'Exception: {e}')
                logging.warning(f'Exception: {e}')
            print("Connection closed.")
            logging.info("Server stopped!\n" + "-" * 20 + "\n")

    def process_msg(self, data):

        char_set = set(list(data))

        if len(char_set) > 0:
            ans = ""
            data = data.split(";")
            for i, req in enumerate(data):
                if req.strip().lower() == "who":
                    ans += self.who() + ";\n   "
                elif req.strip().lower() == "stop":
                    ans += "stop;\n   "
                    return ans
                elif req != "":

                    ans += self.calculate(req) + ";\n   "

                elif i != len(data) - 1:
                    ans += "Empty command;\n   "
            return ans
        else:
            return "Empty command;\n   "

    def calculate(self, data):
        st = set(list(data))
        for char in st:
            if char not in "0123456789*-+/%.^ ":
                return "Wrong Input"
        try:
            ans = str(eval(data))
            self.cnt += 1
            self.sm += float(ans)
            self.mx = max(self.mx, float(ans))
            self.mn = min(self.mn, float(ans))
        except ZeroDivisionError:
            return "Zero Division Error"
        return ans

    def try_connection(self, HOST, PORT):
        try:
            self.server.bind((HOST, PORT))
        except OSError:
            print("Host is used.")
            logging.warning('HOST IS USED.')
            exit()
        self.server.listen(1)

    def final_msg(self):
        if self.cnt != 0:
            x = self.sm / self.cnt
            return f'Results of session:\n\tcount = {self.cnt};' \
                   f'\n\tmin = {self.mn};\n\tmax = {self.mx};\n\taverage = {x};\n\t'
        else:
            return f'Results of session:\n\tcount = {0};' \
                   f'\n\tmin = {None};\n\tmax = {None};\n\taverage = {None};\n\t'

    @staticmethod
    def start_msg():
        return "Write a command or sequence of commands through ';' that will be sent to the server.\n" \
               "For example: '5 + 13; 41/2' and so on.\n" \
               "The words 'who' and 'stop' can be used as a command, " \
               "to get information about the author or stop the session"

    @staticmethod
    def who():
        return 'Fedorych Andrii, K-25, V9, Calculator'


def main():
    Server()


if __name__ == "__main__":
    main()
