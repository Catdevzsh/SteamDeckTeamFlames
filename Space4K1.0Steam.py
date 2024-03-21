import pygame
import sys
from array import array
from random import randint

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Shooting Simulator")

# Colors
BLACK, WHITE, RED, GREEN, BLUE = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)

# Ship and bullet setup
ship_width, ship_height = 60, 20
bullet_width, bullet_height = 5, 10
ship = pygame.Rect(SCREEN_WIDTH // 2 - ship_width // 2, SCREEN_HEIGHT - ship_height - 20, ship_width, ship_height)
bullets = []
targets = []

# Sound generation function
def generate_square_wave(frequency=440, volume=0.1, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    period = int(sample_rate / frequency)
    amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    waveform = array('h', [int(amplitude if time < period / 2 else -amplitude) for time in range(period)] * int(duration * frequency))
    sound = pygame.mixer.Sound(waveform)
    sound.set_volume(volume)
    return sound

# Predefined sounds
hit_target_sound = generate_square_wave(523, 0.1, 0.1)
shoot_sound = generate_square_wave(784, 0.1, 0.05)

# Function to create new targets
def create_target():
    target_width, target_height = 50, 20
    x_position = randint(0, SCREEN_WIDTH - target_width)
    target = pygame.Rect(x_position, 50, target_width, target_height)
    targets.append(target)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and shoot_sound:  # Check if sound is loaded
                bullet = pygame.Rect(ship.centerx - bullet_width // 2, ship.top - bullet_height, bullet_width, bullet_height)
                bullets.append(bullet)
                shoot_sound.play()

    # Ship movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship.left > 0:
        ship.move_ip(-10, 0)
    if keys[pygame.K_RIGHT] and ship.right < SCREEN_WIDTH:
        ship.move_ip(10, 0)

    # Bullet movement
    for bullet in bullets[:]:
        bullet.move_ip(0, -10)
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Bullet and target collision
    for bullet in bullets:
        for target in targets[:]:
            if bullet.colliderect(target):
                if hit_target_sound:  # Ensure the sound is loaded
                    hit_target_sound.play()
                bullets.remove(bullet)
                targets.remove(target)
                break

    # Occasionally add a new target
    if randint(0, 30) == 0:
        create_target()

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, ship)
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)
    for target in targets:
        pygame.draw.rect(screen, GREEN, target)

    pygame.display.flip()
    pygame.time.wait(30)

pygame.quit()
