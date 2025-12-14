#!/usr/bin/env python3
import pygame
import RPi.GPIO as GPIO
import time
import random
import math
from rpi_ws281x import Adafruit_NeoPixel, Color

# ---------------- LED breathing vars -------------
green_level = 20
green_dir = 1
last_update = 0

# ---------------- GPIO ---------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

IN1 = 20
IN2 = 26
GPIO.setup(IN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ---------------- LED STRIP ----------------------
LED_COUNT = 36
BRIGHTNESS = 45
strip = Adafruit_NeoPixel(LED_COUNT, 12, brightness=BRIGHTNESS)
strip.begin()

def set_strip_color(r, g, b):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(r, g, b))
    strip.show()

# ---------------- PYGAME -------------------------
pygame.init()
#screen = pygame.display.set_mode((600, 300))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
pygame.display.set_caption("Reaction Game")

FONT_BIG = pygame.font.SysFont("Arial", 108, bold=True)
FONT_MED = pygame.font.SysFont("Arial", 62)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)

WIDTH, HEIGHT = screen.get_size()
HALF_H = HEIGHT // 2

# ---------------- GAME STATE ---------------------
state = "WAIT_TOUCH"

target_number = 0
start_time = 0
player1_time = None
player2_time = None
white_start = 0

# ---------------- HELPERS ------------------------
def draw_divider():
    thickness = max(4, HEIGHT // 120)
    y = HALF_H - thickness // 2
    pygame.draw.rect(screen, WHITE, (0, y, WIDTH, thickness))

def draw_centered(text, y, inverted=False):
    surf = FONT_MED.render(text, True, WHITE)
    if inverted:
        surf = pygame.transform.rotate(surf, 180)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(surf, rect)

def breathing_green(now):
    global green_level, green_dir, last_update

    STEP = 6
    MIN_L = 20
    MAX_L = 60

    if now - last_update >= 0.063:
        last_update = now
        green_level += STEP * green_dir

        if green_level >= MAX_L:
            green_level = MAX_L
            green_dir = -1
        elif green_level <= MIN_L:
            green_level = MIN_L
            green_dir = 1

        set_strip_color(0, green_level, 0)

def draw_circular_clock(elapsed):
    """
    Рисуем круглые часы на весь экран.
    Стрелка вращается плавно по кругу.
    """
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    radius = min(WIDTH, HEIGHT) // 3

    # Фон круга
    pygame.draw.circle(screen, WHITE, (center_x, center_y), radius, 2)

    # Стрелка
    # Эстетическая анимация: используем синус и косинус для плавного вращения
    angle = (elapsed * math.pi / 3) % (2 * math.pi)  # скорость вращения
    x_end = center_x + int(radius * math.sin(angle))
    y_end = center_y - int(radius * math.cos(angle))  # pygame Y вниз

    pygame.draw.line(screen, WHITE, (center_x, center_y), (x_end, y_end), 4)

    # Опционально: маленький кружок в центре
    pygame.draw.circle(screen, WHITE, (center_x, center_y), 6)


# ---------------- MAIN LOOP ----------------------
clock = pygame.time.Clock()

try:
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise KeyboardInterrupt
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    raise KeyboardInterrupt

        in1 = GPIO.input(IN1)
        in2 = GPIO.input(IN2)

        now = time.time()
        screen.fill(BLACK)

        # -------- WAIT_TOUCH --------
        if state == "WAIT_TOUCH":
            breathing_green(now)

            draw_centered("Коснитесь стола", HALF_H + 40)
            draw_centered("Коснитесь стола", HALF_H - 40, inverted=True)
            draw_divider()
            if in1 == 0 and in2 == 0:
                target_number = random.randint(1, 20)
                state = "SHOW_NUMBER"
                time.sleep(0.3)

        # -------- SHOW_NUMBER -------
        elif state == "SHOW_NUMBER":
            txt = FONT_BIG.render(str(target_number), True, WHITE)

            # нижний игрок
            screen.blit(
                txt,
                txt.get_rect(center=(WIDTH // 2, HALF_H + 65))
            )
            draw_divider()
            # верхний игрок
            screen.blit(
                pygame.transform.rotate(txt, 180),
                txt.get_rect(center=(WIDTH // 2, HALF_H - 65))
            )

            # ждём, пока уберут руки
            if in1 == 1 and in2 == 1:
                white_start = now
                state = "WHITE_SCREEN"

        elif state == "WHITE_SCREEN":
            # Рисуем цифры
            txt = FONT_BIG.render(str(target_number), True, WHITE)
            screen.blit(txt, txt.get_rect(center=(WIDTH // 2, HALF_H + 65)))
            draw_divider()
            screen.blit(
                pygame.transform.rotate(txt, 180),
                txt.get_rect(center=(WIDTH // 2, HALF_H - 65))
            )

            # Прогресс шторы (до середины экрана)
            progress = (now - white_start) / 4.0
            if progress > 1:
                progress = 1

            # Количество полосок
            total_bands = 20
            band_height = HALF_H // total_bands  # делим только половину экрана

            bands_to_draw = int(total_bands * progress)

            for i in range(bands_to_draw):
                # Верхняя полоса
                y_top = i * band_height
                pygame.draw.rect(screen, WHITE, (0, y_top, WIDTH, band_height))
                # Нижняя полоса зеркально
                y_bottom = HEIGHT - (i + 1) * band_height
                pygame.draw.rect(screen, WHITE, (0, y_bottom, WIDTH, band_height))

            # Если шторки сошлись в центре — сразу стартуем тайминг
            if bands_to_draw >= total_bands:
                start_time = now
                player1_time = None
                player2_time = None
                state = "TIMING"
        # стрелка часов начнёт вращаться сразу

        elif state == "TIMING":
            elapsed = now - start_time
            draw_circular_clock(elapsed)

            if in1 == 0 and player1_time is None:
                player1_time = elapsed
            if in2 == 0 and player2_time is None:
                player2_time = elapsed

            if player1_time is not None and player2_time is not None:
                state = "SHOW_RESULT"

        # -------- SHOW_RESULT -------
        elif state == "SHOW_RESULT":
            d1 = abs(player1_time - target_number)
            d2 = abs(player2_time - target_number)
            blink = int(now * 2) % 2

            c1 = WHITE if (d1 < d2 and blink) else GREEN
            c2 = WHITE if (d2 < d1 and blink) else GREEN

            t1 = FONT_MED.render(f"{player1_time:.2f}s", True, c1)
            t2 = FONT_MED.render(f"{player2_time:.2f}s", True, c2)
            draw_divider()
            screen.blit(t1, t1.get_rect(center=(WIDTH // 2, HALF_H + 40)))
            screen.blit(
                pygame.transform.rotate(t2, 180),
                t2.get_rect(center=(WIDTH // 2, HALF_H - 40))
            )

            if in1 == 1 and in2 == 1:
                state = "WAIT_TOUCH"
#        draw_divider()
        pygame.display.flip()
        clock.tick(60)

except KeyboardInterrupt:
    pass
finally:
    set_strip_color(0, 0, 0)
    GPIO.cleanup()
    pygame.quit()
