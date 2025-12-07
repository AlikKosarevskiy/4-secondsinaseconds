#!/usr/bin/env python3
import pygame
import random
import sys
import os
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
BACKGROUND = (240, 240, 240)   # общий фон
TEXT_COLOR = (20, 20, 20)      # общий текст
DIVIDER_COLOR = (80, 80, 80)   # линия между экранами

# --- Шрифты ---
font_size_number = int(min(w, half_h) * 1.2)
if font_size_number < 24:
    font_size_number = 32
font_number = pygame.font.SysFont(None, font_size_number, bold=True)

font_size_start = int(min(w, half_h) * 0.4)
if font_size_start < 18:
    font_size_start = 18
font_start = pygame.font.SysFont(None, font_size_start, bold=True)


# --- Функции ---
def draw_number_dual(n):
    """Рисуем цифру для двух игроков на разделённом экране"""

    # Общий фон
    screen.fill(BACKGROUND)

    # Линия-разделитель
    pygame.draw.rect(screen, DIVIDER_COLOR, (0, half_h - 2, w, 4))

    text = str(n)

    # --- Верхняя половина (перевёрнутая) ---
    rendered_top = font_number.render(text, True, TEXT_COLOR)
    rendered_top = pygame.transform.rotate(rendered_top, 180)
    rect_top = rendered_top.get_rect(center=(w // 2, half_h // 2))
    screen.blit(rendered_top, rect_top)

    # --- Нижняя половина ---
    rendered_bottom = font_number.render(text, True, TEXT_COLOR)
    rect_bottom = rendered_bottom.get_rect(center=(w // 2, half_h + half_h // 2))
    screen.blit(rendered_bottom, rect_bottom)

    pygame.display.flip()


def new_number():
    return random.randint(1, 20)


def show_start_screen_dual():
    """Стартовый экран: две надписи КОСНИТЕСЬ СТОЛА"""
    running_start = True
    clock = pygame.time.Clock()

    while running_start:
        for ev in pygame.event.get():
            if ev.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                running_start = False
            elif ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BACKGROUND)

        # Линия разделитель
        pygame.draw.rect(screen, DIVIDER_COLOR, (0, half_h - 2, w, 4))

        text = "КОСНИТЕСЬ СТОЛА"

        # Верхняя половина (повёрнута)
        txt_top = font_start.render(text, True, TEXT_COLOR)
        txt_top = pygame.transform.rotate(txt_top, 180)
        rect_top = txt_top.get_rect(center=(w // 2, half_h // 2))
        screen.blit(txt_top, rect_top)

        # Нижняя половина
        txt_bottom = font_start.render(text, True, TEXT_COLOR)
        rect_bottom = txt_bottom.get_rect(center=(w // 2, half_h + half_h // 2))
        screen.blit(txt_bottom, rect_bottom)

        pygame.display.flip()
        clock.tick(30)


# --- Показываем стартовый экран ---
show_start_screen_dual()

# --- Основной цикл ---
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
