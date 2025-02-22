import pygame
import random

class Paddle:
    def __init__(self, width, height, x, y):
        self.rect = pygame.Rect(x - width//2, y - height//2, width, height)
        self.speed = 5
        self.x = x  # Store the fixed x position

    def update_position(self, y):
        # Update paddle position while keeping it within screen bounds
        self.rect.centery = min(max(y, self.rect.height//2), 600 - self.rect.height//2)

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)

class Ball:
    def __init__(self, size, x, y):
        self.rect = pygame.Rect(x - size//2, y - size//2, size, size)
        self.speed_x = 7 * random.choice([-1, 1])
        self.speed_y = 7 * random.choice([-1, 1])
        self.reset_pos = (x, y)

    def update(self, player_paddle, bot_paddle, window_width, window_height):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ball collision with top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= window_height:
            self.speed_y *= -1

        # Ball collision with paddles
        if self.rect.colliderect(player_paddle.rect) or self.rect.colliderect(bot_paddle.rect):
            self.speed_x *= -1

        # Reset ball if it goes out of bounds and return score update
        if self.rect.left <= 0:
            self.reset()
            return "left"  # Bot scores
        elif self.rect.right >= window_width:
            self.reset()
            return "right"  # Player scores
        return None

    def reset(self):
        self.rect.center = self.reset_pos
        self.speed_x = 7 * random.choice([-1, 1])
        self.speed_y = 7 * random.choice([-1, 1])

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)

class Bot:
    def __init__(self, paddle, ball):
        self.paddle = paddle
        self.ball = ball
        self.speed = 5

    def update(self):
        # Simple AI: Follow the ball
        if self.ball.rect.centery < self.paddle.rect.centery:
            self.paddle.rect.y -= self.speed
        elif self.ball.rect.centery > self.paddle.rect.centery:
            self.paddle.rect.y += self.speed

        # Keep paddle within screen bounds
        if self.paddle.rect.top < 0:
            self.paddle.rect.top = 0
        elif self.paddle.rect.bottom > 600:
            self.paddle.rect.bottom = 600 