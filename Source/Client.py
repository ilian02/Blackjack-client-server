import socket
import pickle
import sys
import threading
import time

import pygame


SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

pygame.init()
pygame.display.set_caption("Poker with friends")

LOGIN_BUTTON_IMG = pygame.image.load('../Images/button_login.png')
REGISTER_BUTTON_IMG = pygame.image.load('../Images/button_register.png')

# BACKGROUND_IMG = pygame.image.load('../Images/pokerBG2.jpg')
FONT = pygame.font.Font(None, 48)
FONT_LOBBIES = pygame.font.Font(None, 35)
TEXT_COLOUR = (255, 255, 255)
BACKGROUND_COLOR = (1, 50, 32)


class PokerClient:
    """Client Thread that takes care of the client GUI and input"""
    def __init__(self, server_host, server_port):
        self.your_turn = False
        self.game_started = True
        self.run = True
        self.tables = []
        self.logged_in = False
        self.table_name = None
        self.username = None
        self.password = None
        self.current_table = None
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def connect_to_server(self):
        self.client_socket.connect((self.server_host, self.server_port))

    def menu(self):
        """GUI for the main menu for login and register buttons"""

        # self.screen.blit(BACKGROUND_IMG, [0, 0])   # Background image
        self.screen.fill(BACKGROUND_COLOR)  # Temporary background
        self.draw_text("Poker with friends", FONT, TEXT_COLOUR, 450, 150)

        login_button = Button(LOGIN_BUTTON_IMG, 250, 300, 268, 66)
        register_button = Button(REGISTER_BUTTON_IMG, 250, 450, 268, 66)

        self.screen.blit(login_button.image, (login_button.x, login_button.y))
        self.screen.blit(register_button.image, (register_button.x, register_button.y))

        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if login_button.check_if_clicked(pygame.mouse.get_pos()):
                        print("Loading logging page")
                        # self.login_page()
                    if register_button.check_if_clicked(pygame.mouse.get_pos()):
                        print("Loading registering page")
                        # self.register_page()

            pygame.display.update()

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def send_message(self, message):
        # Send a message to the server
        serialized_message = pickle.dumps(message)
        self.client_socket.send(serialized_message)

    def receive_message(self):
        # Receive a message from the server
        serialized_message = self.client_socket.recv(4000)
        return pickle.loads(serialized_message)

    def close_connection(self):
        self.client_socket.close()



class Button:
    """Button class with image and coords"""
    def __init__(self, image, x, y, width, height):
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def check_if_clicked(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height


if __name__ == '__main__':
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 5550

    # Create a PokerClient instance
    poker_client = PokerClient(SERVER_HOST, SERVER_PORT)

    try:
        poker_client.connect_to_server()

        # Implement the game loop or user interface here
        poker_client.menu()

    except KeyboardInterrupt:
        print("Client shutting down.")
    finally:
        poker_client.close_connection()