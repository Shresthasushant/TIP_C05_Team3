import pygame
import subprocess
import sys
import os

# This is to initialize all the pygame modules
pygame.init()
WIDTH, HEIGHT = 800, 600  # The screen size is set to 800 pixels wide and 600 pixels high
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # This sets the display window size
pygame.display.set_caption("Game Launcher")  # This sets the title of the window

# This defines the font and the font size. Default font has been used as denoted by 'none'
FONT_SIZE = 32
font_large = pygame.font.SysFont(None, FONT_SIZE)
font_medium = pygame.font.SysFont(None, FONT_SIZE)

# RGB colors have been used to design the text, background and button colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (135, 206, 250)  # This is the background color (light blue)

# Button size has been defined here to keep all buttons the same size
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 60

# This defines a button, the color of the button and shape of the button.
class Button:
    def __init__(self, text, x, y, w, h, action):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)  # THis creates a rectangular button using x, y position, width and height
        self.color = GRAY
        self.action = action  # Stores the function to be called when the button is clicked

    # This is to show the button on the screen. 'draw' is used to do that.
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font_medium.render(self.text, True, BLACK)  # This shows the text on the button
        text_rect = text_surface.get_rect(center=self.rect.center)  # This puts the text on the button at the center
        surface.blit(text_surface, text_rect)  # This displays the text on the screen

    # This checks if the button has been clicked.
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# This calls a function to run the Arithmetic Card Game
def launch_card_game():
    subprocess.Popen([sys.executable, "card_game.py"])  # Opens card_game.py using the Python interpreter

# This calls a function to run the Spelling Game
def launch_spelling_match_game():
    # This gets the current directory where the launcher file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # This constructs the full path to the spelling match game in 'niharika' subfolder
    game_path = os.path.join(current_dir, "niharika", "main.py")
    # This runs the spelling game
    subprocess.Popen([sys.executable, game_path])

# This function exits the game when the Quit button is clicked
def quit_game():
    pygame.quit()  # This closes all pygame windows
    sys.exit()     # This stops the program

# This is to create buttons for each game and the quit button
buttons = [
    Button("Play Arithmetic Card Game", WIDTH // 2 - BUTTON_WIDTH // 2, 180, BUTTON_WIDTH, BUTTON_HEIGHT, launch_card_game),
    Button("Play Spelling Match Game", WIDTH // 2 - BUTTON_WIDTH // 2, 260, BUTTON_WIDTH, BUTTON_HEIGHT, launch_spelling_match_game),
    Button("Quit", WIDTH // 2 - 50, 360, 100, 50, quit_game),
]

# This makes sure that the launcher keeps on running
running = True
while running:
    screen.fill(BLUE)  # This fills the background color of the window with light blue

    # This is to draw box around the title
    title_box_rect = pygame.Rect(WIDTH // 2 - 200, 50, 400, 60)
    pygame.draw.rect(screen, WHITE, title_box_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, title_box_rect, 2, border_radius=10)

    # This is to draw box around the game buttons
    games_box_rect = pygame.Rect(WIDTH // 2 - 180, 160, 360, 180)
    pygame.draw.rect(screen, WHITE, games_box_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, games_box_rect, 2, border_radius=10)

    # This is to draw box around the Quit button
    quit_button_box_rect = pygame.Rect(WIDTH // 2 - 60, 350, 120, 70)
    pygame.draw.rect(screen, WHITE, quit_button_box_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, quit_button_box_rect, 2, border_radius=10)

    # This is for the title at the center of the launcher
    title_surface = font_large.render("StudiousStars Learning Game", True, BLACK)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, 80))
    screen.blit(title_surface, title_rect)

    # This is to draw the buttons
    for btn in buttons:
        btn.draw(screen)
    pygame.display.flip()  # This updates the screen with everything drawn above

    # This checks for user events such as quitting or mouse clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # This checks if the window's close button is clicked
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # This checks if the mouse is clicked
            for btn in buttons:
                if btn.is_clicked(event.pos):  # If a button is clicked, run its assigned action
                    btn.action()

# This ensures pygame shuts down properly when the program ends
pygame.quit()
sys.exit()
