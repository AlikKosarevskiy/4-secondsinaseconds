#!/usr/bin/env python3
import pygame
import random
import sys
import os
import time
import math

pygame.init()
pygame.mouse.set_visible(False)

# Полноэкранный режим
flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
screen = pygame.display.set_mode((0, 0), flags)
w, h = screen.get_size()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)

# Шрифт
font_size = int(min(w, h) * 0.6)
font = pygame.font.SysFont(None, font_size, bold=True)
small_font = pygame.font.SysFont(None, int(font_size * 0.3), bold=True)

clock = pygame.time.Clock()


# ------------------------------------------------------------
# 📌 Отрисовка стартового экрана с мигающим текстом
# ------------------------------------------------------------
def start_screen():
    blink = True
    blink_timer = 0

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.KEYDOWN:
                return  # старт игры
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        # мигающий текст
        blink_timer += clock.get_time()
        if blink_timer > 500:
            blink = not blink
            blink_timer = 0

        if blink:
            text = small_font.render("КЛАДЕМ РУКИ", True, WHITE)
            rect = text.get_rect(center=(w // 2, h // 2))
            screen.blit(text, rect)

        pygame.display.flip()
        clock.tick(30)


# ------------------------------------------------------------
# 📌 Анимация появления цифры: масштабирование + fade-in
# ------------------------------------------------------------
def animate_number(n):
    duration = 300  # ms
    start_time = pygame.time.get_ticks()

    # создаём текст заранее
    text_surface = font.render(str(n), True, WHITE)
    text_rect = text_surface.get_rect(center=(w // 2, h // 2))

    while True:
        now = pygame.time.get_ticks()
        t = now - start_time
        if t > duration:
            break

        progress = t / duration  # 0.0 → 1.0

        # scale: от 0.1 до 1.0
        scale = 0.1 + 0.9 * progress
        new_w = int(text_rect.width * scale)
        new_h = int(text_rect.height * scale)

        # alpha: от 0 → 255
        alpha = int(255 * progress)

        # создаём уменьшенную копию текста
        frame = pygame.transform.smoothscale(text_surface, (new_w, new_h))
        frame.set_alpha(alpha)

        # центрируем
        frame_rect = frame.get_rect(center=(w // 2, h // 2))

        screen.fill(BLACK)
        screen.blit(frame, frame_rect)
        pygame.display.flip()
        clock.tick(60)

    # после анимации — финальный кадр
    screen.fill(BLACK)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()


# ------------------------------------------------------------
# 📌 Логика выбора случайного числа
# ------------------------------------------------------------
def new_number():
    return random.randint(1, 20)


# ------------------------------------------------------------
# 🚀 СТАРТ
# ------------------------------------------------------------
start_screen()

number = new_number()
animate_number(number)

# ------------------------------------------------------------
# 🎮 Основной игровой цикл
# ------------------------------------------------------------
running = True
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                running = False
            else:
                number = new_number()
                animate_number(number)
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            number = new_number()
            animate_number(number)

    clock.tick(30)

pygame.quit()
sys.exit()
