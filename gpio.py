#!/usr/bin/env python3
import pygame
import RPi.GPIO as GPIO
import time
from rpi_ws281x import Adafruit_NeoPixel, Color

# ---------------- GPIO SETUP ---------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

IN1 = 20
IN2 = 26

GPIO.setup(IN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ---------------- LED STRIP ----------------------
LED_COUNT = 36          # 2 виртуальные ленты по 15 LED
BRIGHTNESS = 45         # треть яркости

# Strip → GPIO 12
strip = Adafruit_NeoPixel(LED_COUNT, 12, brightness=BRIGHTNESS)
strip.begin()

def set_virtual_strip(start, end, r, g, b):
    for i in range(start, end):
        strip.setPixelColor(i, Color(r, g, b))
    strip.show()

# ---------------- PYGAME -------------------------
pygame.init()
pygame.display.set_caption("GPIO Monitor")
screen = pygame.display.set_mode((600, 300))

FONT = pygame.font.SysFont("Arial", 28)

GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def draw_indicator(x, y, label, state):
    color = GREEN if state == 0 else RED
    pygame.draw.circle(screen, color, (x, y), 40)
    text = FONT.render(label, True, WHITE)
    screen.blit(text, (x - text.get_width()//2, y + 50))

# ---------------- MAIN LOOP -----------------------
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt

        in1_state = GPIO.input(IN1)
        in2_state = GPIO.input(IN2)

        # --- Virtual LED strips ---
        if in1_state == 0:
            set_virtual_strip(0, 18, 0, 255, 0)  # зеленый
        else:
            set_virtual_strip(0, 18, 255, 0, 0)  # красный
        
        if in2_state == 0:
            set_virtual_strip(18, 36, 0, 255, 0)
        else:
            set_virtual_strip(18, 36, 255, 0, 0)

        # --- Draw screen ---
        screen.fill(BLACK)

        draw_indicator(150, 100, "Input 1", in1_state)
        draw_indicator(450, 100, "Input 2", in2_state)

        draw_indicator(150, 230, "LED Strip 1", in1_state)
        draw_indicator(450, 230, "LED Strip 2", in2_state)

        pygame.display.update()
        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    # выключаем все LED
    set_virtual_strip(0, LED_COUNT, 0, 0, 0)
    GPIO.cleanup()
    pygame.quit()
