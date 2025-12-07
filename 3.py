#!/usr/bin/env python3
import pygame
import random
import sys
import os
import math
import time

# --- Настройки framebuffer для TFT 3.5" ---
# os.environ["SDL_VIDEODRIVER"] = "fbcon"
# os.environ["SDL_FBDEV"] = "/dev/fb1"

pygame.init()
pygame.mouse.set_visible(False)  # скрыть курсор

# --- Полноэкранное окно ---
flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
screen = pygame.display.set_mode((0, 0), flags)
w, h = screen.get_size()
half_h = h // 2

# --- Цвета ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
YELLOW = (255, 220, 50)

# --- Шрифты ---
font_size_number = int(min(w, half_h) * 1.2)
if font_size_number < 24:
    font_size_number = 32
font_number = pygame.font.SysFont(None, font_size_number, bold=True)

font_size_title = int(min(w, half_h) * 0.3)
if font_size_title < 18:
    font_size_title = 18
font_title = pygame.font.SysFont(None, font_size_title, bold=True)

# --- Функции ---
def draw_number_dual(n):
    """Рисуем цифру для двух игроков на разделённом экране"""
    # Верхняя половина (инвертированная)
    screen.fill(WHITE, rect=(0, 0, w, half_h))
    text = str(n)
    rendered_top = font_number.render(text, True, BLACK)
    rect_top = rendered_top.get_rect(center=(w // 2, half_h // 2))
    # Переворачиваем верхнюю половину
    rendered_top = pygame.transform.rotate(rendered_top, 180)
    rect_top = rendered_top.get_rect(center=(w // 2, half_h // 2))
    screen.blit(rendered_top, rect_top)

    # Нижняя половина (нормальная)
    screen.fill(BLACK, rect=(0, half_h, w, half_h))
    rendered_bottom = font_number.render(text, True, WHITE)
    rect_bottom = rendered_bottom.get_rect(center=(w // 2, half_h + half_h // 2))
    screen.blit(rendered_bottom, rect_bottom)

    pygame.display.flip()

def new_number():
    return random.randint(1, 20)

def show_start_screen():
    """Общий стартовый экран с вращающейся надписью"""
    angle = 0
    running_start = True
    clock = pygame.time.Clock()
    while running_start:
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.KEYDOWN:
                running_start = False
            elif ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLUE)
        text = "СЕКУНДА В СЕКУНДУ"
        rendered_text = font_title.render(text, True, YELLOW)
        rotated_text = pygame.transform.rotate(rendered_text, angle)
        rect = rotated_text.get_rect(center=(w // 2, h // 2))
        screen.blit(rotated_text, rect)

        pygame.display.flip()
        angle = (angle + 2) % 360
        clock.tick(30)

# --- Показываем стартовый экран ---
show_start_screen()

# --- Основной цикл с числами ---
number = new_number()
draw_number_dual(number)

running = True
clock = pygame.time.Clock()
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                running = False
            else:
                number = new_number()
                draw_number_dual(number)
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            number = new_number()
            draw_number_dual(number)
    clock.tick(30)

pygame.quit()
sys.exit()
