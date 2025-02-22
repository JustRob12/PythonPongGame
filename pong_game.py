import pygame
import cv2
import mediapipe as mp
import numpy as np
from hand_tracker import HandTracker
from game_objects import Paddle, Ball, Bot

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 50, 50)

# Set up the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hand-Controlled Pong")

# Initialize game objects
player_paddle = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, 50, WINDOW_HEIGHT//2)
bot_paddle = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, WINDOW_WIDTH-50, WINDOW_HEIGHT//2)
ball = Ball(BALL_SIZE, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
bot = Bot(bot_paddle, ball)

# Initialize hand tracker
hand_tracker = HandTracker()

# Initialize camera
cap = cv2.VideoCapture(0)

# Initialize camera window
cv2.namedWindow('Hand Tracking', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Hand Tracking', 400, 300)

# Initialize scores
player_score = 0
bot_score = 0

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get hand position
    ret, frame = cap.read()
    if ret:
        hand_y, processed_frame = hand_tracker.get_hand_position(frame)
        if hand_y is not None:
            # Directly update paddle position with hand position
            player_paddle.update_position(hand_y)
        
        # Show the camera feed
        cv2.imshow('Hand Tracking', processed_frame)

    # Update game objects
    bot.update()
    score_update = ball.update(player_paddle, bot_paddle, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # Update scores
    if score_update == "left":
        bot_score += 1
    elif score_update == "right":
        player_score += 1

    # Draw everything
    screen.fill(BLACK)
    player_paddle.draw(screen, WHITE)
    bot_paddle.draw(screen, WHITE)
    ball.draw(screen, WHITE)

    # Draw scores
    score_font = pygame.font.Font(None, 74)
    player_text = score_font.render(str(player_score), True, BLUE)
    bot_text = score_font.render(str(bot_score), True, RED)
    screen.blit(player_text, (WINDOW_WIDTH//4, 50))
    screen.blit(bot_text, (3*WINDOW_WIDTH//4, 50))

    pygame.display.flip()
    clock.tick(60)

    # Add key check for quitting
    if cv2.waitKey(1) & 0xFF == ord('q'):
        running = False

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.quit() 