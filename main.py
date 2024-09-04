import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = [(128, 128, 128), (160, 160, 160), (192, 192, 192)]
BACKGROUND_COLOR = WHITE

FONT = pygame.font.SysFont('comicsans', 20)
LARGE_FONT = pygame.font.SysFont('comicsans', 30)
SIDE_PAD = 100
TOP_PAD = 150

class DrawInformation:
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = (self.width - SIDE_PAD) // len(lst)
        self.block_height = (self.height - TOP_PAD) / (self.max_val - self.min_val)
        self.start_x = SIDE_PAD // 2

def draw(draw_info):
    draw_info.window.fill(BACKGROUND_COLOR)
    draw_controls(draw_info)
    draw_list(draw_info)
    pygame.display.update()

def draw_controls(draw_info):
    controls_text = "R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending"
    sorting_text = "I - Insertion Sort | B - Bubble Sort"

    controls = FONT.render(controls_text, 1, BLACK)
    sorting = FONT.render(sorting_text, 1, BLACK)

    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 5))
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 35))

def draw_list(draw_info, color_positions=None, clear_bg=False):
    if color_positions is None:
        color_positions = {}

    if clear_bg:
        clear_rect = (SIDE_PAD // 2, TOP_PAD, draw_info.width - SIDE_PAD, draw_info.height - TOP_PAD)
        pygame.draw.rect(draw_info.window, BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(draw_info.lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        color = color_positions.get(i, GRAY[i % len(GRAY)])
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height - y))

    if clear_bg:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(n)]

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)

    for i in range(n - 1):
        for j in range(n - 1 - i):
            if (lst[j] > lst[j + 1] and ascending) or (lst[j] < lst[j + 1] and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: GREEN, j + 1: RED}, True)
                yield True
    yield False

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algo = bubble_sort
    sorting_algo_gen = None

    while run:
        clock.tick(120)

        if sorting:
            try:
                sorting = next(sorting_algo_gen)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    lst = generate_starting_list(n, min_val, max_val)
                    draw_info.set_list(lst)
                    sorting = False
                elif event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    sorting_algo_gen = sorting_algo(draw_info, ascending)
                elif event.key == pygame.K_a and not sorting:
                    ascending = True
                elif event.key == pygame.K_d and not sorting:
                    ascending = False

    pygame.quit()

if __name__ == "__main__":
    main()
