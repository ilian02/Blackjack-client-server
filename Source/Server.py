import pickle
import socket
import threading


class BlackJackServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.playing_tables = []
        self.account_handler = None
        self.deck = None

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        print(f'Server is listening on {self.host}:{self.port}')

        try:
            while True:
                client_socket, address = server_socket.accept()
                client_handler_thread = threading.Thread(target=self.handle_client, args=(client_socket))
                client_handler_thread.start()
        except KeyboardInterrupt:
            print("Shutting down server")
        finally:
            server_socket.close()

    def handle_client(self, client_socket):
        try:
            # Receive client_name from the client
            while True:
                message = pickle.loads(client_socket.recv(4000))
                client_socket.send(pickle.dumps({'message': 'You have sent a message'}))
        except Exception as e:
            print(f'Error handling client: {e}')
        finally:
            client_socket.close()


if __name__ == '__main__':
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 5550

    blackjack_server = BlackJackServer(SERVER_HOST, SERVER_PORT)
    blackjack_server.start()