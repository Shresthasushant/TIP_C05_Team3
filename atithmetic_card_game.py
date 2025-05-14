import pygame
import random
import sys

# This is to initialize all the pygame modules
pygame.init()
WIDTH, HEIGHT = 800, 600  # This sets the width and height of the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # This is to display the game window
pygame.display.set_caption("Arithmetic Card Game")  # This is to display the window title

# This is to define the font and the font size. Default font has been used as denoted by 'None'
font_large = pygame.font.SysFont(None, 36)
font_medium = pygame.font.SysFont(None, 24)

# RGB colors have been used to design the text and the button colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (200, 200, 200)
BLUE = (135, 206, 250)  # Light blue background

# This defines a button, the color of the button and shape of the button
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text  # This stores the button text
        self.rect = pygame.Rect(x, y, w, h)  # This creates a rectangle for the button
        self.color = GRAY  # This sets the default color of the button

    # This is to show the button on the screen. 'draw' is used to do that
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)  # This draws the button shape
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=8)  # This draws the border for visibility
        text_surface = font_medium.render(self.text, True, BLACK)  # This shows the button text
        text_rect = text_surface.get_rect(center=self.rect.center)  # This centers the text on the button
        surface.blit(text_surface, text_rect)  # This puts the text on the screen

    # This checks if the button has been clicked
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)  # This returns True if the click was inside the button

# This defines the global variables
correct_answer = 0
buttons = []
feedback_text = ""
feedback_color = BLACK
next_question_time = 0
score = 0
high_score = 0
game_over = False
last_score = 0  # This stores the score when the game is over after the user enters a wrong answer
try_again_button = Button("Try Again", WIDTH // 2 - 100, 250, 100, 50)  # This creates the Try Again button
exit_button = Button("Quit", WIDTH // 2 + 10, 250, 100, 50)  # This creates the Quit button after the wrong answer.

# This defines a function 'new_question' to ask the arithmetic question
def new_question():
    global correct_answer, buttons, feedback_text, feedback_color

    feedback_text = ""  # This clears previous feedback
    number1 = random.randint(1, 10)
    number2 = random.randint(1, 10)
    operation = random.choice(['+', '-', '*'])  # This randomly chooses an arithmetic operator

    # This performs the selected arithmetic operation
    if operation == '+':
        correct_answer = number1 + number2
    elif operation == '-':
        correct_answer = number1 - number2
    else:
        correct_answer = number1 * number2

    question = f"What is {number1} {operation} {number2}?"  # This prepares the question string

    # This randomly chooses the correct answer position
    correct_pos = random.randint(0, 2)
    answers = []

    for i in range(3):
        if i == correct_pos:
            answers.append(correct_answer)  # This inserts the correct answer
        else:
            wrong = correct_answer + random.choice([-3, -2, -1, 1, 2, 3])
            while wrong == correct_answer or wrong in answers:
                wrong = correct_answer + random.choice([-3, -2, -1, 1, 2, 3])  # This avoids duplicate or correct values
            answers.append(wrong)

    # This creates buttons for the answer options
    buttons.clear()
    total_button_width = 3 * 100 + 2 * 50  # 3 buttons, 2 gaps of 50px
    start_x = (WIDTH - total_button_width) // 2  # This centers the buttons horizontally
    for i in range(3):
        btn = Button(str(answers[i]), start_x + i * 150, 200, 100, 50)
        buttons.append(btn)

    # This adds a Quit button
    quit_btn = Button("Quit", WIDTH - 110, HEIGHT - 60, 100, 40)
    buttons.append(quit_btn)

    return question

# This calls the function again to ask the first question and run the program
question_text = new_question()
# This creates a click to play button to start the game
start_button = Button("Click to Play", WIDTH // 2 - 75, HEIGHT // 2, 150, 50)

# This shows the start screen for the user to start playing
show_start_screen = True
while show_start_screen:
    screen.fill(BLUE)

    # This is to display the title
    title_text = font_large.render("Arithmetic Card Game", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

    # This is to draw the start button
    start_button.draw(screen)

    pygame.display.flip()

    for event in pygame.event.get():  # This checks all events happening in the game
        if event.type == pygame.QUIT:  # This checks if the player clicked the close button
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.is_clicked(event.pos):  # This checks if the start button is clicked
                show_start_screen = False  # This exits the start screen to start the game
                pygame.event.clear()  # This clears any pending events, including the initial mouse click event

# This is to start the game loop.
running = True
while running:
    screen.fill(BLUE)  # This sets the background color to blue

    if not game_over:
        # This displays the arithmetic question
        text_surface = font_large.render(question_text, True, BLACK)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 80))

        # This displays the current score and high score
        score_text = font_medium.render(f"Score: {score}  High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (20, 20))

        # This draws all the answer and quit buttons
        for btn in buttons:
            btn.draw(screen)

        # This shows feedback text if present
        if feedback_text:
            fb_surface = font_medium.render(feedback_text, True, feedback_color)
            screen.blit(fb_surface, (WIDTH // 2 - fb_surface.get_width() // 2, 300))
    else:
        # This shows the Game Over screen
        game_over_text = font_large.render("Game Over!", True, RED)
        final_score_text = font_medium.render(f"Your Score: {last_score}", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 100))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, 150))

        # This draws the Try Again and Quit buttons on Game Over screen
        try_again_button.draw(screen)
        exit_button.draw(screen)

    pygame.display.flip()  # This updates the screen

    for event in pygame.event.get():  # This checks all the events happening in the game
        if event.type == pygame.QUIT:  # This checks if the player clicked the close button
            running = False  # This stops the game

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                # This checks if the player clicked Try Again or Quit on the Game Over screen
                if try_again_button.is_clicked(event.pos):
                    score = 0  # This resets the score to 0
                    game_over = False  # This switches off the game over state
                    feedback_text = ""  # This clears the feedback text
                    feedback_color = BLACK  # This resets feedback color
                    question_text = new_question()  # This asks a new question
                    next_question_time = 0  # This resets the timer for the next question
                elif exit_button.is_clicked(event.pos):
                    running = False  # This quits the game when 'Quit' is clicked
            else:
                # This block is executed when the game is not over
                if next_question_time == 0:
                    for btn in buttons:
                        if btn.is_clicked(event.pos):
                            if btn.text == "Quit":
                                running = False  # This exits the game when the quit button is clicked
                                break
                            elif int(btn.text) == correct_answer:
                                feedback_text = "Correct!"  # This gives correct feedback
                                feedback_color = GREEN  # This sets feedback color to green
                                score += 1  # This increases the score for correct answer
                                if score > high_score:
                                    high_score = score  # This updates the high score if current score is higher
                            else:
                                feedback_text = "Wrong!"  # This gives wrong feedback
                                feedback_color = RED  # This sets feedback color to red
                                last_score = score  # This saves the score before reset
                                score = 0  # This resets score on wrong answer
                                game_over = True  # This triggers the game over state
                            next_question_time = pygame.time.get_ticks() + 1000  # This adds delay before the next question

    # This handles the transition to the next question after delay
    if next_question_time != 0 and pygame.time.get_ticks() >= next_question_time and not game_over:
        question_text = new_question()  # This asks a new question
        next_question_time = 0  # This resets the timer

pygame.quit()  # This ends the pygame session
sys.exit()  # This exits the program completely
