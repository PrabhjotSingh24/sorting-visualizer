import pygame
import random


pygame.init()


class DrawInformation:
    black = 0, 0, 0
    white = 255, 255, 255
    green = 0, 255, 0
    red = 255, 0, 0
    grey = 128, 128, 128
    bg = white
    shades_of_grey = (grey, (160, 160, 160), (100, 100, 100))
    # padding from right and left
    padding = 100
    # top padding for the controls
    top_padding = 125

    font = pygame.font.SysFont("Poppins regular", 25)
    head_font = pygame.font.SysFont("Poppins semibold", 30)

    def __init__(self, width, height, lst) -> None:
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algo Visualizer")
        self.set_list(lst)

    def set_list(self, lst: list):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width-self.padding)/len(lst))
        self.block_height = (self.height-self.top_padding) / \
            (self.max_val-self.min_val)
        self.start_x = self.padding//2


def list_gen(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst


def draw(draw_info: DrawInformation,sorting_algo,ascending):
    # available_algos=SortingAlgos(draw_info)
    draw_info.window.fill(draw_info.bg)
    controls = draw_info.font.render(
        "R-reset | SPACE-start sorting | A-ascending | D-descending", True, draw_info.black)
    draw_info.window.blit(
        controls, ((draw_info.width-controls.get_width())//2, 10))
    controls2 = draw_info.font.render(
        "B-Bubble Sort | I-Insertion Sort | S-Selection Sort", True, draw_info.black)
    draw_info.window.blit(
        controls2, ((draw_info.width-controls2.get_width())//2, controls.get_height() + 15))
    controls3=draw_info.head_font.render(
        f"{sorting_algo} - {ascending}", True, draw_info.black)
    draw_info.window.blit(
        controls3, ((draw_info.width-controls3.get_width())//2, controls2.get_height() + 40))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info: DrawInformation, color_positions={}, clear_bg=False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.padding//2, draw_info.top_padding, draw_info.width -draw_info.padding, draw_info.height-draw_info.top_padding)
        pygame.draw.rect(draw_info.window, draw_info.bg, clear_rect)
    for i, val in enumerate(lst):
        x = draw_info.start_x+i*draw_info.block_width
        y = draw_info.height-(val-draw_info.min_val) * draw_info.block_height
        color = draw_info.shades_of_grey[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color,(x, y, draw_info.block_width, draw_info.height))
    if clear_bg:
        pygame.display.update()


class SortingAlgos:
    def __init__(self, draw_info: DrawInformation) -> None:
        self.draw_info = draw_info


    def bubble_sort(self, ascending=True):
        lst = self.draw_info.lst

        for i in range(len(lst)-1):
            for j in range(len(lst)-1-i):
                if (lst[j] > lst[j+1] and ascending) or (lst[j] > lst[j+1] and not ascending):
                    lst[j], lst[j+1] = lst[j+1], lst[j]
                    draw_list(self.draw_info, {j: self.draw_info.green, i: self.draw_info.red}, True)
                    yield True
        return lst

    def insertion_sort(self, ascending=True):
        lst = self.draw_info.lst

        for i in range(1, len(lst)):
            current_rect = lst[i]
            while True:
                ascending_sort = i > 0 and lst[i -1] > current_rect and ascending
                descending_sort = i > 0 and lst[i -1] < current_rect and not ascending

                if not ascending_sort and not descending_sort:
                    break
                lst[i] = lst[i-1]
                i = i-1
                lst[i] = current_rect
                draw_list(self.draw_info, {i-1: self.draw_info.green, i: self.draw_info.red}, True)
                yield True
        return lst

    def selection_sort(self, ascending):
        lst = self.draw_info.lst
        indexing_length = range(0, len(lst)-1)
        for i in indexing_length:
            min_value_index = i
            for j in range(i+1, len(lst)):
                if lst[j] < lst[min_value_index]:
                    min_value_index = j
            draw_list(self.draw_info, {
                i-1: self.draw_info.green, i: self.draw_info.red}, True)
            if min_value_index != i:
                lst[i], lst[min_value_index] = lst[min_value_index], lst[i]
            yield True
        return lst


def main():
    fps = pygame.time.Clock()
    n = 100
    min_val = 0
    max_val = 100
    run = True
    sorting = False
    ascending = True
    lst = list_gen(n, min_val, max_val)
    draw_rects = DrawInformation(500, 500, lst)
    sorting_algorithm_name="Bubble Sort"
    sorting_algorithm_generator = SortingAlgos(draw_rects).bubble_sort(ascending=ascending)
    while run:
        fps.tick(120)
        if sorting:
            try:
                sorting_algorithm_generator.__next__()
            except StopIteration:
                sorting = False
        else:
            draw(draw_rects,sorting_algorithm_name,ascending)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = list_gen(n, max_val=max_val, min_val=min_val)
                draw_rects.set_list(lst)
                sorting = False
            if event.key == pygame.K_SPACE and sorting == False :
                sorting = True
            if event.key == pygame.K_a and not sorting:
                ascending = True
            if event.key == pygame.K_d and not sorting:
                ascending = False
            if event.key==pygame.K_b and not sorting:
                sorting_algorithm_name="Bubble Sort"
                sorting_algorithm_generator = SortingAlgos(draw_rects).bubble_sort(ascending=ascending)
            if event.key==pygame.K_i and not sorting:
                sorting_algorithm_name="Insertion Sort"
                sorting_algorithm_generator = SortingAlgos(draw_rects).insertion_sort(ascending=ascending)
            if event.key==pygame.K_s and not sorting:
                sorting_algorithm_name="Selection Sort"
                sorting_algorithm_generator = SortingAlgos(draw_rects).selection_sort(ascending=ascending)
    pygame.quit()


if __name__ == "__main__":
    main()
