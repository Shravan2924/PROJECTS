import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Hockey")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define game modes
AI_GAME = 1
COMPUTER_GAME = 2

# Load background image
background_image = pygame.image.load("1.jpg")  # Replace "background.jpg" with your image file

# Define functions for game modes
def launch_ai_game():
    import ai_game
    ai_game.main()

def launch_computer_game():
    import computer_game
    computer_game.main()

# Main opening screen loop
def opening_screen():
    font = pygame.font.SysFont(None, 48)

    selection_text = font.render("Select Game Mode:", True, WHITE)
    ai_text = font.render("1 Player (AI)", True, WHITE)
    computer_text = font.render("2. TWO Plaayers", True, WHITE)

    selection_text_rect = selection_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    ai_text_rect = ai_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    computer_text_rect = computer_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    launch_ai_game()
                elif event.key == pygame.K_2:
                    launch_computer_game()

        screen.blit(background_image, (0, 0))  # Draw background image
        screen.blit(selection_text, selection_text_rect)
        screen.blit(ai_text, ai_text_rect)
        screen.blit(computer_text, computer_text_rect)
        pygame.display.flip()

if __name__ == "__main__":
    opening_screen()
