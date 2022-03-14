import pygame
from random import randint

SIZE_W = (25, 22)
TALL = 23
BLOCK = TALL + 2
LEFT, RIGHT, DOWN, UP = range(4)
LOSE, OK = range(2)
sc = pygame.display.set_mode((SIZE_W[0] * BLOCK, SIZE_W[1] * BLOCK))


def check(snake: list, block: list):
    for blockOfSnake in snake:
        if blockOfSnake[:2] == block:
            return LOSE
    return OK


def grown(snake: list):
    p = snake[-1]
    if p[2] == LEFT:
        snake.append([p[0] + 1, p[1], p[2]])
    elif p[2] == RIGHT:
        snake.append([p[0] - 1, p[1], p[2]])
    elif p[2] == UP:
        snake.append([p[0], p[1] + 1, p[2]])
    else:
        snake.append([p[0], p[1] - 1, p[2]])


def press(snake: list):
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
    if snake[2] == LEFT:
        if snake[0] - 1 < 0 or check(all_snake, [snake[0] - 1, snake[1]]) == LOSE:
            return LOSE
        snake[0] -= 1
    elif snake[2] == RIGHT:
        if snake[0] + 1 >= SIZE_W[0] or check(all_snake, [snake[0] + 1, snake[1]]) == LOSE:
            return LOSE
        snake[0] += 1
    elif snake[2] == UP:
        if snake[1] - 1 < 0 or check(all_snake, [snake[0], snake[1] - 1]) == LOSE:
            return LOSE
        snake[1] -= 1
    else:
        if snake[1] + 1 >= SIZE_W[1] or check(all_snake, [snake[0], snake[1] + 1]) == LOSE:
            return LOSE
        snake[1] += 1
    return OK


def game(snake: list, apple: list, game_: bool):
    if game_:
        last = snake[0][2]
        for i in range(len(snake)):
            if move(snake[i], snake) == LOSE:
                return LOSE
            pygame.draw.rect(sc, "white", [snake[i][0] * BLOCK, snake[i][1] * BLOCK, TALL, TALL])
            last, snake[i][2] = snake[i][2], last
        press(snake)
    if snake[0][:2] == apple:
        p = LOSE
        while p == LOSE:
            apple[0] = randint(0, SIZE_W[0] - 1)
            apple[1] = randint(0, SIZE_W[1] - 1)
            p = check(snake, apple)
        grown(snake)
    pygame.draw.rect(sc, "red", [apple[0] * BLOCK, apple[1] * BLOCK, BLOCK, BLOCK])

    return game_


def main():
    pygame.init()
    clock = pygame.time.Clock()

    snake = [[9, 9, RIGHT], ]
    play, pc = OK, 4
    apple = [randint(0, SIZE_W[0] - 1), randint(0, SIZE_W[1] - 1)]

    while play or pc:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        sc.fill("black")
        play = game(snake, apple, play)
        if not play:
            pc -= 1
            for i in range(len(snake)):
                pygame.draw.rect(sc, "white", [snake[i][0] * BLOCK, snake[i][1] * BLOCK, TALL, TALL])
        pygame.display.update()
        clock.tick(12)


if __name__ == '__main__':
    main()
    pygame.quit()
