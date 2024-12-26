import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Perang Pesawat Tempur")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load assets
player_img = pygame.image.load("player.png")  # Replace with your image file
enemy_img = pygame.image.load("enemy.png")    # Replace with your image file
bullet_img = pygame.image.load("bullet.png")  # Replace with your image file

# Scale images
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet_center = Bullet(self.rect.centerx, self.rect.top)
        bullet_left = Bullet(self.rect.centerx - 15, self.rect.top)
        bullet_right = Bullet(self.rect.centerx + 15, self.rect.top)
        
        all_sprites.add(bullet_center, bullet_left, bullet_right)
        bullets.add(bullet_center, bullet_left, bullet_right)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_multiplier=1):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 2) * speed_multiplier

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            global game_over
            game_over = True

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Groups
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Game variables
score = 0
level = 1
enemies_to_kill = 10
speed_multiplier = 1
game_over = False
show_start_screen = True

# Spawn initial enemies
def spawn_enemies(num_enemies):
    for _ in range(num_enemies):
        enemy = Enemy(speed_multiplier)
        all_sprites.add(enemy)
        enemies.add(enemy)

def calculate_enemy_count(level):
    return max(5 - level, 1)

spawn_enemies(calculate_enemy_count(level))

# Font
font = pygame.font.SysFont("Arial", 24)
game_over_font = pygame.font.SysFont("Arial", 48)

# Function to reset the game
def reset_game():
    global score, level, game_over, speed_multiplier, player
    score = 0
    level = 1
    game_over = False
    speed_multiplier = 1
    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    player = Player()
    all_sprites.add(player)
    spawn_enemies(calculate_enemy_count(level))

# Game loop
running = True
while running:
    if show_start_screen:
        # Display start screen
        screen.fill(BLACK)
        title_text = game_over_font.render("Perang Pesawat Tempur", True, WHITE)
        start_text = font.render("Press ENTER to Start", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        # Wait for start
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key to start
                    show_start_screen = False

    else:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.shoot()
                if game_over:
                    if event.key == pygame.K_r:
                        reset_game()
                    elif event.key == pygame.K_q:
                        running = False

        if not game_over:
            # Update
            all_sprites.update()

            # Collision detection
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                score += 1
                if score % enemies_to_kill == 0:
                    level += 1
                    speed_multiplier += 0.5
                    spawn_enemies(calculate_enemy_count(level))

                # Spawn new enemy
                enemy = Enemy(speed_multiplier)
                all_sprites.add(enemy)
                enemies.add(enemy)

        # Draw
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Display score and level
        if not game_over:
            score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
            screen.blit(score_text, (10, 10))
        else:
            game_over_text = game_over_font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))

            instructions_text = game_over_font.render("Press R to Restart or Q to Quit", True, WHITE)
            screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        clock.tick(FPS)

pygame.quit()
