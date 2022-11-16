from socket import *
import logging


class Client:
    def __init__(self,):
        try:
            HOST = '192.168.1.38'
            PORT = 1025 + 9

            logging.getLogger("Client")
            logging.basicConfig(filename="client_log.log",
                                level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                filemode='w',
                                )

            logging.info("Client socket created")

            client = socket(
                AF_INET, SOCK_STREAM,
            )
            # print(client.getblocking())

            client.connect((HOST, PORT))
            logging.info(f'Connected to a server {HOST}')
            data = client.recv(256).decode('utf-8')
            print(data)

            while True:
                msg = "=" + input('Send request:\n=')
                client.send(msg.encode('utf-8'))

                logging.info(f'Sent request: {msg}')

                data = client.recv(256).decode('utf-8')
                logging.info(f'Received answer: {data}')
                print('Answer:\n ', data)

                if "stop" in data:
                    logging.info(f'Connection closed')
                    client.close()
                    break

            print("Connection closed.")

        except Exception as exp:
            logging.exception(f"Happened exception: {exp}. The server may be down.")
            print(f"Happened exception: {exp}. The server may be down.")


def main():
    Client()


if __name__ == "__main__":
    main()
