from random import randint
import pygame
import pygame_menu
import sys

pygame.init()
background_img = pygame.image.load('snake-logo.jpg')
SIZE_BLOCK = 20
FRAME_COLOR = (0, 255, 204)
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
RED = (255, 0, 0)
SNAKE_COLOR = (0, 102, 0)
HEADER_COLOR = (0, 204, 153)
HEADER_MARGIN = 70
COUNT_BLOCKS = 20
MARGIN = 1
size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 36)


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # head in snake_blocks
    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y






def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [
        SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
        HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
        SIZE_BLOCK, SIZE_BLOCK])


def start_the_game():

    def get_random_empty_block():
        x = randint(0, COUNT_BLOCKS - 1)
        y = randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = randint(0, COUNT_BLOCKS - 1)
            empty_block.y = randint(0, COUNT_BLOCKS - 1)
        return empty_block
    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    new_dot = get_random_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    total = 0
    speed = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        text_total = courier.render(f'Total: {total}', 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        text_speed = courier.render(f'Speed: {speed}', 0, WHITE)
        screen.blit(text_speed, (240, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE
                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            print('crash')
            break
        draw_block(RED, new_dot.x, new_dot.y)

        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        if new_dot == head:
            total += 1
            speed = total // 5 + 1
            snake_blocks.append(new_dot)
            new_dot = get_random_empty_block()

        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            print('crash yourself')
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(3 + speed)



main_theme = pygame_menu.themes.THEME_DARK.copy()
main_theme.set_background_color_opacity(0.4)
menu = pygame_menu.Menu('', 300, 220,
                       theme=main_theme)

menu.add.text_input('Name :', default='Player 1')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

while True:
    screen.fill(WHITE)
    screen.blit(pygame.transform.scale(background_img, [640, 800]), (-140, -200))

    events = pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    if menu.is_enabled():
        menu.update(events)
        menu.draw((screen))
    pygame.display.update()
