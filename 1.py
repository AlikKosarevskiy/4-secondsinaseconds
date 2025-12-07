#!/usr/bin/env python3
import pygame
import random
import sys
import os

# Если используешь framebuffer-версию дисплея (часто /dev/fb1),
# можно раскомментировать и установить переменные окружения здесь:
# os.environ["SDL_VIDEODRIVER"] = "fbcon"
# os.environ["SDL_FBDEV"] = "/dev/fb1"
# os.environ["SDL_MOUSEDRV"] = "TSLIB"   # иногда нужно для тачскрина
# os.environ["TSLIB_FBDEVICE"] = "/dev/fb1"
# os.environ["TSLIB_TSDEVICE"] = "/dev/input/event0"  # проверь своё устройство

pygame.init()
pygame.mouse.set_visible(False)  # скрыть курсор

# Попробуем открыть полноэкранное окно
flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
screen = pygame.display.set_mode((0, 0), flags)  # (0,0) -> fullscreen
w, h = screen.get_size()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Подбираем размер шрифта в зависимости от разрешения
# Для 3.5" TFT обычно 480x320 — шрифт будет крупным.
font_size = int(min(w, h) * 0.6)
if font_size < 24:
    font_size = 24
font = pygame.font.SysFont(None, font_size, bold=True)

def draw_number(n):
    screen.fill(BLACK)
    text = str(n)
    # если число маленькое, можно увеличить вес/обводку: отрисуем тень
    rendered = font.render(text, True, WHITE)
    rect = rendered.get_rect(center=(w // 2, h // 2))

    # тень (чуть смещённая чёрная подложка)
    shadow = font.render(text, True, (30, 30, 30))
    shadow_rect = shadow.get_rect(center=(w // 2 + 4, h // 2 + 4))
    screen.blit(shadow, shadow_rect)

    screen.blit(rendered, rect)
    pygame.display.flip()

def new_number():
    return random.randint(1, 20)

number = new_number()
draw_number(number)

clock = pygame.time.Clock()

# Основной цикл: по тапу или клавише обновляем число
running = True
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            # ESC — выход; любая другая клавиша -> новое число
            if ev.key == pygame.K_ESCAPE:
                running = False
            else:
                number = new_number()
                draw_number(number)
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            # касание тачскрина генерирует MOUSEBUTTONDOWN
            number = new_number()
            draw_number(number)
        # на некоторых конфигурациях тачскрина приходят TOUCH события вместо MOUSE,
        # но Pygame обычно преобразует их в MOUSEBUTTONDOWN.

    clock.tick(30)

pygame.quit()
sys.exit()
