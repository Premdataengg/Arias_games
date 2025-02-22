import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions (Increased resolution)
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Ice Cream!")

# Load images
background = pygame.image.load("background.jpg")  # Use a light-themed ice cream shop background
cone_img = pygame.image.load("cone.png")  # Cone sprite
scoop_img = pygame.image.load("scoop.png")  # Ice cream scoop sprite
rock_img = pygame.image.load("rock.png")  # Rock sprite

# Resize images
cone_img = pygame.transform.scale(cone_img, (80, 100))
scoop_img = pygame.transform.scale(scoop_img, (50, 50))
rock_img = pygame.transform.scale(rock_img, (50, 50))

# Game variables
cone = pygame.Rect(WIDTH // 2 - 40, HEIGHT - 110, 80, 100)
objects = []
obstacles = []
bullets = []
score = 0
game_over = False

# Fonts
font = pygame.font.Font(None, 50)
game_over_font = pygame.font.Font(None, 70)

# Sound effects
catch_sound = pygame.mixer.Sound("catch.wav")  # Play sound when catching a scoop
hit_sound = pygame.mixer.Sound("hit.wav")  # Play sound when hitting a rock
shoot_sound = pygame.mixer.Sound("catch.wav")  # Sound for shooting bullets

# Clock
clock = pygame.time.Clock()


# Functions
def spawn_scoop():
    x = random.randint(20, WIDTH - 50)
    objects.append(pygame.Rect(x, 0, 50, 50))


def spawn_obstacle():
    x = random.randint(20, WIDTH - 50)
    obstacles.append(pygame.Rect(x, 0, 50, 50))


def move_objects():
    global score
    for obj in objects[:]:
        obj.y += 4
        if obj.colliderect(cone):
            objects.remove(obj)
            score += 1
            catch_sound.play()
        elif obj.y > HEIGHT:
            objects.remove(obj)


def move_obstacles():
    global game_over
    for obs in obstacles[:]:
        obs.y += 5
        if obs.colliderect(cone):
            game_over = True
            hit_sound.play()
        elif obs.y > HEIGHT:
            obstacles.remove(obs)


def move_bullets():
    for bullet in bullets[:]:
        bullet.y -= 10
        if bullet.y < 0:
            bullets.remove(bullet)
        for obs in obstacles[:]:
            if bullet.colliderect(obs):
                obstacles.remove(obs)
                bullets.remove(bullet)
                break


def draw_game():
    screen.blit(background, (0, 0))  # Draw background

    # Draw ice cream scoops
    for obj in objects:
        screen.blit(scoop_img, (obj.x, obj.y))

    # Draw rocks
    for obs in obstacles:
        screen.blit(rock_img, (obs.x, obs.y))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 0, 0), bullet)

    # Draw cone
    screen.blit(cone_img, (cone.x, cone.y))

    # Display score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))


# Main loop
running = True
spawn_timer = 0

while running:
    screen.fill((255, 255, 255))
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet = pygame.Rect(cone.x + cone.width // 2 - 5, cone.y, 10, 20)
            bullets.append(bullet)
            shoot_sound.play()

    # Move cone with mouse
    mouse_x, _ = pygame.mouse.get_pos()
    cone.x = max(0, min(WIDTH - cone.width, mouse_x - cone.width // 2))

    # Spawn scoops and obstacles
    spawn_timer += 1
    if spawn_timer % 40 == 0:
        spawn_scoop()
    if spawn_timer % 80 == 0:
        spawn_obstacle()

    move_objects()
    move_obstacles()
    move_bullets()
    draw_game()

    # Game over screen
    if game_over:
        screen.fill((255, 0, 0, 150))
        text = game_over_font.render("GAME OVER!", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 - 50))
        pygame.display.update()
        pygame.time.delay(2000)
        break

    pygame.display.update()

pygame.quit()
