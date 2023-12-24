
import sys
import pygame
import random
import ctypes
import math
from PIL import ImageGrab

# Constants
FPS = 60
ARROW_SPEED = 8

BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Santa's Adventure")
clock = pygame.time.Clock()

user32 = ctypes.windll.user32
WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# Initialize Pygame
pygame.init()


# Load start button images
start_button_img = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT))
start_button_img.fill(WHITE)
exit_button_img = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT))
exit_button_img.fill(WHITE)

# Fonts
font = pygame.font.Font(None, 36)

# Get screen resolution
user32 = ctypes.windll.user32
SCREEN_WIDTH, SCREEN_HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
start_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
start_button_y = (SCREEN_HEIGHT - BUTTON_HEIGHT) // 2
exit_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
exit_button_y = start_button_y + 100

start_button_rect = start_button_img.get_rect(topleft=(start_button_x, start_button_y))
exit_button_rect = exit_button_img.get_rect(topleft=(exit_button_x, exit_button_y))

# Load game image
game_image = pygame.image.load('game_image.png')
game_image = pygame.transform.scale(game_image, (600, 400))
game_rect = game_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

# pygame.mixer.init()
pygame.mixer.music.load('christmas_music.mp3')
pygame.mixer.music.play(-1)

# Get current desktop wallpaper as background
background = ImageGrab.grab(bbox=(0, 0, WIDTH, HEIGHT))
background = background.resize((WIDTH, HEIGHT))

# Load Santa cart image
santa_img = pygame.image.load('santa_cart_image.png')
santa_img = pygame.transform.scale(santa_img, (100, 100))

# Load arrow image
arrow_img = pygame.image.load('arrow_image.png')
arrow_img = pygame.transform.scale(arrow_img, (40, 20))

# Load bow image
bow_img = pygame.image.load('bow_image.png')
bow_img = pygame.transform.scale(bow_img, (80, 80))


# Start window loop
start_window = True
while start_window:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                start_window = False
            elif exit_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    screen.blit(game_image, game_rect)
    pygame.draw.rect(screen, BLACK, start_button_rect)
    pygame.draw.rect(screen, BLACK, exit_button_rect)
    start_button_text = font.render("Start", True, WHITE)
    exit_button_text = font.render("Exit", True, WHITE)
    screen.blit(start_button_text, (start_button_x + 70, start_button_y + 15))
    screen.blit(exit_button_text, (exit_button_x + 75, exit_button_y + 15))


    pygame.display.flip()
# Load victory sound
victory_sound = pygame.mixer.Sound('victory_sound.mp3')  # Replace with your victory sound file path

# Initialize game variables
arrow_count = 69
hit_count = 0

# Health counter
health = 5


class SantaCart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = santa_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-HEIGHT, 0)  # Start Santas randomly above the screen
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(-HEIGHT, 0)
            self.rect.x = random.randint(0, WIDTH - self.rect.width)

# Arrow class
class Arrow(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()
        self.image = arrow_img
        self.rect = self.image.get_rect(center=start_pos)
        self.angle = 0
        self.dx = 0
        self.dy = 0
        self.shooting = False

    def update(self):
        if self.shooting:
            self.rect.x += self.dx
            self.rect.y += self.dy

            if not (0 <= self.rect.x <= WIDTH and 0 <= self.rect.y <= HEIGHT):
                self.kill()

    def shoot(self, mouse_pos):
        self.angle = math.atan2(mouse_pos[1] - self.rect.centery, mouse_pos[0] - self.rect.centerx)
        self.dx = ARROW_SPEED * math.cos(self.angle)
        self.dy = ARROW_SPEED * math.sin(self.angle)
        self.shooting = True

# Bow class
class Bow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bow_img
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.centery = HEIGHT // 2

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_pos[1] - self.rect.centery, mouse_pos[0] - self.rect.centerx)
        self.image = pygame.transform.rotate(bow_img, math.degrees(-self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

# Snowflake class
class Snowflake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(-HEIGHT, 0)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(-HEIGHT, 0)
            self.rect.x = random.randint(0, WIDTH)

# Gift class
class Gift(pygame.sprite.Sprite):
    def __init__(self, santa_rect):
        super().__init__()
        self.image = pygame.image.load('gift_image.png')
        self.image = pygame.transform.scale(self.image, (40, 40))  #
        self.rect = self.image.get_rect(center=santa_rect.center)
        self.dy = 3

    def update(self):
        self.rect.y += self.dy
        if self.rect.y > HEIGHT:
            self.kill()

all_sprites = pygame.sprite.Group()
santas = pygame.sprite.Group()
arrows = pygame.sprite.Group()
bow = Bow()
all_sprites.add(bow)
snowflakes = pygame.sprite.Group()

for _ in range(100):
    snowflake = Snowflake()
    snowflakes.add(snowflake)


# Main game loop
game_over = False
victory = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if arrow_count > 0:
                arrow = Arrow(bow.rect.center)
                arrow.shoot(pygame.mouse.get_pos())
                arrows.add(arrow)
                arrow_count -= 1



    screen.fill((0, 0, 0))  # Fill the screen with black

    all_sprites.update()
    arrows.update()
    snowflakes.update()

    # Create new Santas if the count is low
    while len(santas) < 5:
        new_santa = SantaCart()
        santas.add(new_santa)
        all_sprites.add(new_santa)

    # Check for arrow collisions with Santas
    for arrow in arrows:
        hit_list = pygame.sprite.spritecollide(arrow, santas, True)
        if hit_list:
            hit_count += 5
            arrow_count += 1
            arrow_count += 1
            for santa in hit_list:
                gift = Gift(santa.rect)
                all_sprites.add(gift)

    # Check if Santa touches the bottom of the screen
    for santa in santas:
        if santa.rect.bottom >= HEIGHT:
            health -= 1
            santa.kill()

    # Check game over condition
    if health <= 0:
        game_over = True

    if hit_count >= 500:
        victory = True

    if game_over:
        game_over_text = font.render("Game Over  - Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
        pygame.display.flip()
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset game variables
                        health = 3
                        hit_count = 0
                        arrow_count = 69
                        for santa in santas:
                            santa.kill()
                            new_santa = SantaCart()
                            santas.add(new_santa)
                            all_sprites.add(new_santa)
                        game_over = False
                    elif event.key == pygame.K_q:
                        running = False
                        game_over = False

    if victory:
        victory_text = ("You successfully stole the Christmas. "
                        "\n**** You have been awarded medal of appachchi ****"
                        " \nMarry Cristmas!")

        lines = victory_text.split('\n')
        line_height = 40

        for i, line in enumerate(lines):



            pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2))
            font_victory = pygame.font.Font(None, 48)
            victory_surface = font.render(line, True, (255, 255, 255))

            screen.blit(victory_surface, (50, 50 + i * line_height))


        pygame.display.flip()

        # Play victory sound
        victory_sound.play()

        while victory:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        victory = False

                    elif event.key == pygame.K_r:
                        # Reset game variables
                        health = 3
                        hit_count = 0
                        arrow_count = 50
                        for santa in santas:
                            santa.kill()
                            new_santa = SantaCart()
                            santas.add(new_santa)
                            all_sprites.add(new_santa)
                        game_over = False

    # Set desktop wallpaper as background
    background_image = pygame.image.fromstring(background.tobytes(), background.size, background.mode)

    # Draw on the transparent surface
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    arrows.draw(screen)
    snowflakes.draw(screen)

    # Show dashboard
    pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT - 80, WIDTH, 80))  # Background for dashboard
    arrow_text = font.render(f"Arrows Left: {arrow_count}", True, WHITE)
    hit_text = font.render(f"Hits: {hit_count}", True, WHITE)
    health_text = font.render(f"Health: {health}", True, WHITE)
    screen.blit(arrow_text, (20, HEIGHT - 70))
    screen.blit(hit_text, (WIDTH - 200, HEIGHT - 70))
    screen.blit(health_text, (WIDTH // 2 - 50, HEIGHT - 70))

    pygame.display.flip()
    clock.tick(FPS)


    pygame.display.flip()

pygame.quit()
