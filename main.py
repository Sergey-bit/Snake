import pygame
from random import randint

SIZE_W = (25, 22)
TALL = 23
BLOCK = TALL + 2
LEFT, RIGHT, DOWN, UP = range(4)
LOSE = 0
FUNCS = {
    LEFT: lambda x, y: [x + 1, y, LEFT],
    RIGHT: lambda x, y: [x - 1, y, RIGHT],
    UP: lambda x, y: [x, y + 1, UP],
    DOWN: lambda x, y: [x, y - 1, DOWN],
}
sc = pygame.display.set_mode((SIZE_W[0] * BLOCK, SIZE_W[1] * BLOCK))

def draw(snake, apple):
    for i in range(len(snake)):
        pygame.draw.rect(sc, "white", [snake[i][0] * BLOCK, snake[i][1] * BLOCK, TALL, TALL])
    pygame.draw.rect(sc, "red", [apple[0] * BLOCK, apple[1] * BLOCK, BLOCK, BLOCK])

def check(snake, block):
    for blockOfSnake in snake:
        if blockOfSnake[:2] == block:
            return 1
    return 0

def press(snake):
    key = pygame.key.get_pressed()
    last = snake[0][2]
    if key[pygame.K_d] and last not in (RIGHT, LEFT):
        snake[0][2] = RIGHT
    elif key[pygame.K_w] and last not in (UP, DOWN):
        snake[0][2] = UP
    elif key[pygame.K_a] and last not in (RIGHT, LEFT):
        snake[0][2] = LEFT
    elif key[pygame.K_s] and last not in (UP, DOWN):
        snake[0][2] = DOWN

def move(snake, all_snake):
    global LOSE
    if snake[2] == LEFT:
        if snake[0] - 1 < 0 or check(all_snake, [snake[0] - 1, snake[1]]):
            LOSE = 1
        snake[0] -= 1 - LOSE
    elif snake[2] == RIGHT:
        if snake[0] + 1 >= SIZE_W[0] or check(all_snake, [snake[0] + 1, snake[1]]):
            LOSE = 1
        snake[0] += 1 - LOSE
    elif snake[2] == UP:
        if snake[1] - 1 < 0 or check(all_snake, [snake[0], snake[1] - 1]):
            LOSE = 1
        snake[1] -= 1 - LOSE
    else:
        if snake[1] + 1 >= SIZE_W[1] or check(all_snake, [snake[0], snake[1] + 1]):
            LOSE = 1
        snake[1] += 1 - LOSE

def game(snake, apple):
    last = snake[0][2]
    for i in range(len(snake)):
        move(snake[i], snake)
        last, snake[i][2] = snake[i][2], last
    press(snake)
    if snake[0][:2] == apple:
        p = 1
        while p:
            apple[0], apple[1] = randint(0, SIZE_W[0] - 1), randint(0, SIZE_W[1] - 1)
            p = check(snake, apple)
        snake.append(FUNCS[snake[-1][2]](*snake[-1][:2]))

def main():
    pygame.init()
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock().tick

    snake = [[9, 9, RIGHT], ]
    apple = [randint(0, SIZE_W[0] - 1), randint(0, SIZE_W[1] - 1)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        sc.fill("black")
        if not LOSE:
            game(snake, apple)
        elif pygame.key.get_pressed()[pygame.K_SPACE]:
            break
        draw(snake, apple)
        pygame.display.update()
        clock(12)
    pygame.quit()


if __name__ == '__main__':
    main()
