import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Hockey")

# Load background image
background_image = pygame.image.load("2.jpg")  # Replace "2.jpg" with your image file

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)  # Light gray color for scoreboard
BLACK = (0, 0, 0)  # Define the BLACK color constant

# Define game elements
class Paddle:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 20, 100)
        self.color = color
        self.speed = 10  # Increased speed
        self.direction = 0  # 0 for not moving, -1 for up, 1 for down

    def update(self):
        self.rect.y += self.direction * self.speed
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Puck:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = BLACK  # Initial color of the puck
        self.speed_x = 7
        self.speed_y = 7
        self.glow_rate = 5  # Rate of color transition
        self.glowing_up = True  # Flag to indicate if glowing is increasing or decreasing
        self.collision_point = None  # Point of collision with paddle

    def update_color(self):
        if self.glowing_up:
            self.color = (min(self.color[0] + self.glow_rate, 255),
                          min(self.color[1] + self.glow_rate, 255),
                          min(self.color[2] + self.glow_rate, 255))
            if self.color == (255, 255, 255):  # If reached maximum brightness, start decreasing
                self.glowing_up = False
        else:
            self.color = (max(self.color[0] - self.glow_rate, 0),
                          max(self.color[1] - self.glow_rate, 0),
                          max(self.color[2] - self.glow_rate, 0))
            if self.color == (0, 0, 0):  # If reached minimum brightness, start increasing
                self.glowing_up = True

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Check for collisions with top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y = -self.speed_y

    def draw(self):
        pygame.draw.ellipse(screen, self.color, self.rect)
        if self.collision_point:
            pygame.draw.line(screen, WHITE, self.rect.center, self.collision_point, 2)

# Define game states
class GameState:
    START_SCREEN = 0
    PLAYING = 1
    GAME_OVER = 2

# Define the SCORE_LIMIT constant
SCORE_LIMIT = 5  # Adjust this value as needed

# Main game loop
def main():
    game_state = GameState.START_SCREEN

    player1_paddle = Paddle(50, HEIGHT // 2 - 50, RED)
    player2_paddle = Paddle(WIDTH - 70, HEIGHT // 2 - 50, BLUE)
    puck = Puck(WIDTH // 2 - 10, HEIGHT // 2 - 10)

    player1_score = 0
    player2_score = 0

    font = pygame.font.SysFont(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_state == GameState.START_SCREEN:
                    game_state = GameState.PLAYING
                elif game_state == GameState.PLAYING:
                    # Player 1 controls
                    if event.key == pygame.K_w:
                        player1_paddle.direction = -1
                    elif event.key == pygame.K_s:
                        player1_paddle.direction = 1
                    # Player 2 controls
                    elif event.key == pygame.K_UP:
                        player2_paddle.direction = -1
                    elif event.key == pygame.K_DOWN:
                        player2_paddle.direction = 1
            elif event.type == pygame.KEYUP:
                if game_state == GameState.PLAYING:
                    # Player 1 controls
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        player1_paddle.direction = 0
                    # Player 2 controls
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player2_paddle.direction = 0

        if game_state == GameState.PLAYING:
            # Update game state
            player1_paddle.update()
            player2_paddle.update()
            puck.update()

            # Check for collisions with paddles
            if player1_paddle.rect.colliderect(puck.rect) or player2_paddle.rect.colliderect(puck.rect):
                puck.speed_x = -puck.speed_x

            # Check for goals
            if puck.rect.left <= 0:
                player2_score += 1
                reset_game(player1_paddle, player2_paddle, puck)
            elif puck.rect.right >= WIDTH:
                player1_score += 1
                reset_game(player1_paddle, player2_paddle, puck)

            # Check for game over condition
            if player1_score >= SCORE_LIMIT or player2_score >= SCORE_LIMIT:
                game_state = GameState.GAME_OVER

        # Render
        screen.blit(background_image, (0, 0))  # Draw background image
        # Draw game elements
        player1_paddle.draw()
        player2_paddle.draw()
        puck.draw()

        # Draw scores with light gray color
        player1_score_text = font.render("Player 1: " + str(player1_score), True, BLACK)
        player2_score_text = font.render("Player 2: " + str(player2_score), True, BLACK)
        screen.blit(player1_score_text, (20, 20))
        screen.blit(player2_score_text, (WIDTH - 170, 20))

        pygame.display.flip()  # Update the display

        # Cap the frame rate
        pygame.time.Clock().tick(60)

        # Check for game over condition and reset the game if necessary
        if game_state == GameState.GAME_OVER:
            game_over(player1_score, player2_score)
            player1_score = 0
            player2_score = 0
            reset_game(player1_paddle, player2_paddle, puck)

def reset_game(player1_paddle, player2_paddle, puck):
    puck.rect.center = (WIDTH // 2, HEIGHT // 2)
    player1_paddle.rect.center = (50, HEIGHT // 2)
    player2_paddle.rect.center = (WIDTH - 70, HEIGHT // 2)
    puck.speed_x = 7 if random.randint(0, 1) == 0 else -7
    puck.speed_y = random.choice([-7, 7])

def game_over(player1_score, player2_score):
    # Load background image for game over screen
    game_over_background = pygame.image.load("3.jpg")  # Replace "3.jpg" with your image file
    game_over_background = pygame.transform.scale(game_over_background, (WIDTH, HEIGHT))  # Scale the image to fit the screen

    # Display game over screen with a background image
    screen.blit(game_over_background, (0, 0))  # Blit the background image onto the screen
    font = pygame.font.SysFont(None, 48)
    winner_text = font.render("Player 1 Wins!" if player1_score > player2_score else "Player 2 Wins!", True, WHITE)
    player1_score_text = font.render("Player 1 Score: " + str(player1_score), True, WHITE)
    player2_score_text = font.render("Player 2 Score: " + str(player2_score), True, WHITE)

    # Calculate text positions
    winner_text_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    player1_score_text_rect = player1_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    player2_score_text_rect = player2_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    # Blit text onto the screen
    screen.blit(winner_text, winner_text_rect)
    screen.blit(player1_score_text, player1_score_text_rect)
    screen.blit(player2_score_text, player2_score_text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)  # Delay for 3 seconds to allow players to see the final scores

if __name__ == "__main__":
    main()
