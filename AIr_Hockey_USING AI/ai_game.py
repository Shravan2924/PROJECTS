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
        self.color = WHITE  # Initial color of the puck
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

def move_ai_paddle(ai_paddle, puck):
    if puck.rect.centery < ai_paddle.rect.centery:
        ai_paddle.direction = -1
    elif puck.rect.centery > ai_paddle.rect.centery:
        ai_paddle.direction = 1
    else:
        ai_paddle.direction = 0

def check_paddle_collision(paddle, puck):
    if paddle.rect.colliderect(puck.rect):
        # Calculate collision point based on the side of the paddle
        if puck.speed_x > 0:  # Puck moving to the right
            collision_x = WIDTH - puck.rect.width // 2  # Collision point on the right wall
        else:  # Puck moving to the left
            collision_x = puck.rect.width // 2  # Collision point on the left wall
        collision_y = HEIGHT // 2  # Collision point at the center of the window

        puck.collision_point = (collision_x, collision_y)
        puck.speed_x = -puck.speed_x
    else:
        puck.collision_point = None

def reset_game(player_paddle, ai_paddle, puck):
    puck.rect.center = (WIDTH // 2, HEIGHT // 2)
    player_paddle.rect.center = (50, HEIGHT // 2)
    ai_paddle.rect.center = (WIDTH - 70, HEIGHT // 2)
    puck.speed_x = random.choice([-7, 7])
    puck.speed_y = random.choice([-7, 7])

def check_goal(player_paddle, puck):
    if puck.rect.left <= 0:
        return True
    elif puck.rect.right >= WIDTH:
        return True
    return False

# Define the SCORE_LIMIT constant
SCORE_LIMIT = 2  # Adjust this value as needed

# Main game loop
def start_screen():
    # Load the background image for the start screen
    start_screen_background = pygame.image.load("1.jpg")
    start_screen_background = pygame.transform.scale(start_screen_background, (WIDTH, HEIGHT))

    font = pygame.font.SysFont(None, 72)
    title_text = font.render("Air Hockey", True, WHITE)
    start_text = font.render("Press any key to start", True, WHITE)

    title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(start_screen_background, (0, 0))  # Corrected line
    screen.blit(title_text, title_text_rect)
    screen.blit(start_text, start_text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

# Heuristic function for AI paddle movement
def heuristic(player_paddle, ai_paddle, puck):
    # Calculate the distance between the puck and the center of the AI paddle
    distance = abs(puck.rect.centery - ai_paddle.rect.centery)

    # If the puck is far from the AI paddle, move the paddle towards the center
    if distance > 20:
        if puck.rect.centery < ai_paddle.rect.centery:
            ai_paddle.direction = -1
        elif puck.rect.centery > ai_paddle.rect.centery:
            ai_paddle.direction = 1
    # If the puck is close to the AI paddle, try to intercept it
    else:
        if puck.rect.centery < ai_paddle.rect.centery:
            ai_paddle.direction = -1
        elif puck.rect.centery > ai_paddle.rect.centery:
            ai_paddle.direction = 1
        else:
            ai_paddle.direction = 0

# Main game loop
def main():
    start_screen()

    player_paddle = Paddle(50, HEIGHT // 2 - 50, RED)
    ai_paddle = Paddle(WIDTH - 70, HEIGHT // 2 - 50, BLUE)
    puck = Puck(WIDTH // 2 - 10, HEIGHT // 2 - 10)

    player_score = 0
    ai_score = 0

    font = pygame.font.SysFont(None, 36)

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    player_paddle.direction = -1
                elif event.key == pygame.K_DOWN:
                    player_paddle.direction = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_paddle.direction = 0

        # Update game state
        heuristic(player_paddle, ai_paddle, puck)  # Call the heuristic function
        player_paddle.update()
        ai_paddle.update()
        puck.update()
        check_paddle_collision(player_paddle, puck)
        check_paddle_collision(ai_paddle, puck)
        puck.update_color()

        # Check if the puck is out of bounds
        if puck.rect.left <= 0:
            ai_score += 1
            reset_game(player_paddle, ai_paddle, puck)
        elif puck.rect.right >= WIDTH:
            player_score += 1
            reset_game(player_paddle, ai_paddle, puck)

        # Check for game over condition
        if player_score >= SCORE_LIMIT or ai_score >= SCORE_LIMIT:
            game_over(player_score, ai_score)
            player_score = 0
            ai_score = 0
            reset_game(player_paddle, ai_paddle, puck)

        # Render
        screen.blit(background_image, (0, 0))  # Draw background image
        # Draw game elements
        player_paddle.draw()
        ai_paddle.draw()
        puck.draw()

        # Draw scores with light gray color
        player_score_text = font.render("Player: " + str(player_score), True, BLACK)
        ai_score_text = font.render("Computer: " + str(ai_score), True, BLACK)
        screen.blit(player_score_text, (20, 20))
        screen.blit(ai_score_text, (WIDTH - 170, 20))

        # Draw boundary lines
        pygame.draw.line(screen, WHITE, (0, 0), (WIDTH, 0), 2)  # Top boundary line
        pygame.draw.line(screen, WHITE, (0, HEIGHT), (WIDTH, HEIGHT), 2)  # Bottom boundary line

        pygame.display.flip()  # Update the display

        # Cap the frame rate
        pygame.time.Clock().tick(60)

def game_over(player_score, ai_score):
    # Load background image for game over screen
    game_over_background = pygame.image.load("3.jpg")  # Replace "3.jpg" with your image file
    game_over_background = pygame.transform.scale(game_over_background, (WIDTH, HEIGHT))  # Scale the image to fit the screen

    # Display game over screen with a background image
    screen.blit(game_over_background, (0, 0))  # Blit the background image onto the screen
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render("Game Over", True, WHITE)
    player_score_text = font.render("Player Score: " + str(player_score), True, WHITE)
    ai_score_text = font.render("Computer Score: " + str(ai_score), True, WHITE)
    # Calculate text positions
    game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    player_score_text_rect = player_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    ai_score_text_rect = ai_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    # Blit text onto the screen
    screen.blit(game_over_text, game_over_text_rect)
    screen.blit(player_score_text, player_score_text_rect)
    screen.blit(ai_score_text, ai_score_text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)  # Delay for 3 seconds to allow players to see the final scores

if __name__ == "__main__":
    main()
