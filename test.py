import os
import sys
import pygame
import random

screen_rect = (0, 0, 800, 800)
pygame.init()
pygame.display.set_caption('2048')
screen = pygame.display.set_mode((800, 800))


# загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# класс для "кнопок"
class Button:
    # создание кнопки
    def create_button(self, surface, color, x, y, length, height, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x, y, length, height)
        return surface

    # добавление текста на кнопку
    def write_text(self, surface, text, text_color, length, height, x, y):
        myText = font2.render(text, 1, text_color)
        surface.blit(myText, ((x + length / 2) - myText.get_width() / 2, (y + height / 2) - myText.get_height() / 2))
        return surface

    # отрисовка кнопки
    def draw_button(self, surface, color, length, height, x, y):
        sur = pygame.Surface((length, height), pygame.SRCALPHA)
        pygame.draw.rect(sur, pygame.Color(color), (0, 0, length, height), 0)
        screen.blit(sur, (x, y))
        return surface

    # нажатие на кнопку
    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
        return False


# игровое поле
class Board:
    # создание поля
    def __init__(self, list, score=0):
        if len(list) > 1:
            self.board = list
        else:
            self.board = self.gen_board()
        self.colors = {'2': '#33FFFF', '4': '#33CCFF', '8': '#33CCCC',
                       '16': '#3399FF', '32': '#3399CC',
                       '64': '#3366FF', '128': '#3333FF', '256': '#3333FF',
                       '512': '#3300FF', '1024': '#3333CC', '2048': '#3300CC'}
        self.score = score

    # генерация поля
    def gen_board(self):
        board = [[0] * 5 for _ in range(5)]
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        x1 = random.randint(0, 4)
        y1 = random.randint(0, 4)
        if (x == x1) and (y == y1):
            if x != 0:
                x -= 1
            else:
                x += 1
        board[x][y] = 2
        board[x1][y1] = 2
        return board

    # смещение блоков налево
    def move_left(self):
        for i in self.board:
            while 0 in i:
                i.remove(0)
            while len(i) != 5:
                i.append(0)
        for i in range(5):
            for j in range(4):
                if self.board[i][j] == self.board[i][j + 1] and self.board[i][j] != 0:
                    self.board[i][j] *= 2
                    self.score += self.board[i][j]
                    self.board[i].pop(j + 1)
                    self.board[i].append(0)

    # смещение блоков направо
    def move_right(self):
        for i in self.board:
            while 0 in i:
                i.remove(0)
            while len(i) != 5:
                i.insert(0, 0)
        for i in range(5):
            for j in range(4, 0, -1):
                if self.board[i][j] == self.board[i][j - 1] and self.board[i][j] != 0:
                    self.board[i][j] *= 2
                    self.score += self.board[i][j]
                    self.board[i].pop(j - 1)
                    self.board[i].insert(0, 0)

    # смещение блоков вверх
    def move_up(self):
        new_matix = [[0] * 5 for _ in range(5)]
        for i in range(5):
            for j in range(5):
                new_matix[j][i] = self.board[i][j]
        for i in new_matix:
            while 0 in i:
                i.remove(0)
            while len(i) != 5:
                i.append(0)
        for i in range(5):
            for j in range(4):
                if new_matix[i][j] == new_matix[i][j + 1] and new_matix[i][j] != 0:
                    new_matix[i][j] *= 2
                    self.score += new_matix[i][j]
                    new_matix[i].pop(j + 1)
                    new_matix[i].append(0)
        self.board.clear()
        self.board = [[0] * 5 for _ in range(5)]
        for i in range(5):
            for j in range(5):
                self.board[j][i] = new_matix[i][j]

    # смещение блоков вниз
    def move_down(self):
        new_matix = [[0] * 5 for _ in range(5)]
        for i in range(5):
            for j in range(5):
                new_matix[j][i] = self.board[i][j]
        for i in new_matix:
            while 0 in i:
                i.remove(0)
            while len(i) != 5:
                i.insert(0, 0)
        for i in range(5):
            for j in range(4, 0, -1):
                if new_matix[i][j] == new_matix[i][j - 1] and new_matix[i][j] != 0:
                    new_matix[i][j] *= 2
                    self.score += new_matix[i][j]
                    new_matix[i].pop(j - 1)
                    new_matix[i].insert(0, 0)
        self.board.clear()
        self.board = [[0] * 5 for _ in range(5)]
        for i in range(5):
            for j in range(5):
                self.board[j][i] = new_matix[i][j]

    # получить текущий счёт
    def get_score(self):
        return self.score

    def get_board(self):
        return self.board

    # появление нового блока
    def new_block(self):
        f = False
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == 0:
                    f = True
        while f:
            x, y = random.randint(0, 4), random.randint(0, 4)
            if self.board[x][y] == 0:
                f = False
                self.board[x][y] = random.choice([2, 4])
        self.render(screen)
        pygame.display.flip()

    # проигрыш
    def losing(self):
        f = 0
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == 0:
                    return False
                if j != 4:
                    if self.board[i][j] == self.board[i][j + 1]:
                        f = 1
                if j != 0:
                    if self.board[i][j] == self.board[i][j - 1]:
                        f = 1
                if i != 0:
                    if self.board[i][j] == self.board[i - 1][j]:
                        f = 1
                if i != 4:
                    if self.board[i][j] == self.board[i + 1][j]:
                        f = 1
                if f == 1:
                    return False
        return True

    # победа
    def winn(self):
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == 2048:
                    return True
        return False

    # отрисовка поля
    def render(self, screen):
        s = pygame.Surface((600, 600), pygame.SRCALPHA)
        sur = pygame.Surface((108, 108), pygame.SRCALPHA)
        pygame.draw.rect(s, pygame.Color((20, 20, 20)), (0, 0, 600, 600), 0)
        screen.blit(s, (100, 100))
        for i in range(5):
            for j in range(5):
                x = 10 * (j + 1) + 108 * j + 100
                y = 10 * (i + 1) + 108 * i + 100
                if self.board[i][j] == 0:
                    text = ''
                    color = (25, 25, 25)
                else:
                    color = self.colors[str(self.board[i][j])]
                    text = str(self.board[i][j])
                pygame.draw.rect(sur, pygame.Color(color), (0, 0, 108, 108), 0)
                screen.blit(sur, (x, y))
                if text:
                    font_size = 108 // 3
                    font = pygame.font.SysFont('cambria', font_size)
                    myText = font.render(text, 1, pygame.Color('white'))
                    screen.blit(myText, (x + 54 - myText.get_width() / 2, y + 54 - myText.get_height() / 2))


# для закрытия окна
def terminate():
    pygame.quit()
    sys.exit()


# заставка игры
def start_screen():
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('segoeuiblack', 80)
    string_rendered = font.render('2048', 1, pygame.Color('white'))
    screen.blit(string_rendered, (300, 60))
    button = Button()
    button.create_button(screen, (25, 25, 25, 127), 250, 210, 300, 80, 'Новая игра', (255, 255, 255))

    button2 = Button()
    button2.create_button(screen, (25, 25, 25, 127), 250, 330, 300, 80, 'Продолжить игру', (255, 255, 255))

    button3 = Button()
    button3.create_button(screen, (25, 25, 25, 127), 250, 450, 300, 80, 'Правила игры', (255, 255, 255))

    button4 = Button()
    button4.create_button(screen, (25, 25, 25, 127), 250, 570, 300, 80, 'Турнирная таблица', (255, 255, 255))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button3.pressed(event.pos):
                    pygame.display.flip()
                    rules_window()
                    return
                if button4.pressed(event.pos):
                    pygame.display.flip()
                    tourney_window()
                    return
                if button.pressed(event.pos):
                    pygame.display.flip()
                    new_game_window()
                    return
                if button2.pressed(event.pos):
                    pygame.display.flip()
                    game(0)
                    return
        pygame.display.flip()


# окно инициализации пользователя(ввод имени)
def new_game_window():
    screen.blit(fon, (0, 0))
    text = font.render('Введите свой ник', 1, pygame.Color('white'))
    screen.blit(text, (220, 40))
    button_back.create_button(screen, (25, 25, 25, 127), 450, 650, 300, 80, 'Вернуться назад', (255, 255, 255))
    sur = pygame.Surface((300, 50), pygame.SRCALPHA)
    pygame.draw.rect(sur, pygame.Color(25, 25, 25), (0, 0, 300, 50), 0)
    screen.blit(sur, (250, 300))
    warning = font2.render('Максимальный размер ника - 20 символов', 1, pygame.Color('white'))
    screen.blit(warning, (200, 360))
    new_game_button = Button()
    new_game_button.create_button(screen, (25, 25, 25, 127), 50, 650, 300, 80, 'Начать игру', (255, 255, 255))
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.pressed(event.pos):
                    start_screen()
                if new_game_button.pressed(event.pos) and len(text) > 1:
                    game(1, text)
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) <= 20:
                        text += str(event.unicode)
                    else:
                        pass
                if len(text) < 21:
                    pygame.draw.rect(sur, pygame.Color(25, 25, 25), (0, 0, 300, 50), 0)
                    screen.blit(sur, (250, 300))
                    txt_surface = font2.render(text, True, pygame.Color('white'))
                    screen.blit(txt_surface, (250, 310))
                else:
                    pass
            pygame.display.flip()


# непосредственная игра
def game(flag, name=False):
    with open('outfile.txt') as f:
        read_data = [(i.rstrip('/n')).split() for i in f.readlines()]
    a = ([[int(j) for j in i] for i in read_data[:-2]])
    if len(a) > 1 and flag == 0:
        name = read_data[-1][0]
        score = int(read_data[-2][0])
    if flag == 1:
        f = open("outfile.txt", 'w')
        f.write('')
        f.close()
        a = []
        score = 0
    if (flag == 1) or (len(a) > 1 and flag == 0):
        screen.blit(fon, (0, 0))
        board = Board(a, score)
        board.render(screen)
        score = str(board.get_score())
        font3 = pygame.font.SysFont('segoeuiblack', 30)
        score_text = font3.render("Score:" + score + ' ', True, (0, 0, 0), (255, 255, 255))
        screen.blit(score_text, (100, 50))
        button_menu = Button()
        name_text = font3.render("Name:" + name + ' ', True, (0, 0, 0), (255, 255, 255))
        screen.blit(name_text, (330, 50))
        button_menu.create_button(screen, (25, 25, 25, 127),
                                  160, 720, 500, 70, 'Сохранить игру и вернуться в главное меню', (255, 255, 255))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        board.move_left()
                        board.render(screen)
                        board.new_block()
                    if event.key == pygame.K_RIGHT:
                        board.move_right()
                        board.render(screen)
                        board.new_block()
                    if event.key == pygame.K_UP:
                        board.move_up()
                        board.render(screen)
                        board.new_block()
                    if event.key == pygame.K_DOWN:
                        board.move_down()
                        board.render(screen)
                        board.new_block()
                    score = str(board.get_score())
                    score_text = font3.render("Score:" + score + ' ', True, (0, 0, 0), (255, 255, 255))
                    screen.blit(score_text, (100, 50))
                    pygame.display.flip()
                    if board.winn():
                        board.render(screen)
                        file = open("tourner.txt", 'a')
                        file.write(str(name) + ' ' + str(score) + '\n')
                        file.close()
                        if flag == 0:
                            f = open("outfile.txt", 'w')
                            f.write('')
                            f.close()
                        pygame.time.delay(2500)
                        game_over(score, 1)
                        return
                    if board.losing():
                        board.render(screen)
                        if flag == 0:
                            f = open("outfile.txt", 'w')
                            f.write('')
                            f.close()
                        file = open("tourner.txt", 'a')
                        file.write(str(name) + ' ' + str(score) + '\n')
                        file.close()
                        pygame.time.delay(2500)
                        game_over(score, 0)
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_menu.pressed(event.pos):
                        remember_board = board.get_board()
                        f = open("outfile.txt", 'w')
                        for i in remember_board:
                            for j in i:
                                f.write(str(j) + ' ')
                            f.write('\n')
                        f.write(score)
                        f.write('\n')
                        f.write(name)
                        f.close()
                        start_screen()
                        return
            pygame.display.flip()
    else:
        start_screen()
        return


# завершение игры
def game_over(score, f):
    screen.blit(fon, (0, 0))
    if f == 1:
        text = font.render('YOUR WINN!!!', True, (184, 134, 11))
        image = load_image("winn.png", -1)
        screen.blit(image, (800 // 2 - image.get_width() / 2, 0))
    else:
        text = font.render('GAME OVER', True, (255, 0, 0))
    screen.blit(text, (800 // 2 - text.get_width() / 2, 800 // 2 - text.get_height() / 2))
    text2 = font.render('Your score:' + score, True, (255, 255, 255))
    screen.blit(text2, (800 // 2 - text2.get_width() / 2, 800 // 2 - text.get_height() / 2 + 100))
    button_menu = Button()
    button_menu.create_button(screen, (25, 25, 25, 127),
                              250, 650, 300, 80, 'Вернуться в главное меню', (255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_menu.pressed(event.pos):
                    start_screen()
                    return
        pygame.display.flip()


# правила игры
def rules_window():
    screen.blit(fon, (0, 0))
    intro_text = ['Цель игры - собрать кирпичек с цифрой «2048».',
                  "В начале игры вам выдается два кирпичика с цифрой «2», нажимая",
                  "кнопочки вверх, вправо, влево или вниз, ",
                  "все ваши кирпичики будут смещаться в ту же сторону.",
                  "При соприкосновении клеточек с одним и тем же номиналом, ",
                  "они объединяются и создают сумму вдвое больше.",
                  'Игра заканчивается тогда, когда все пустые ячейки заполнены,',
                  'и вы больше не можете передвигать клеточки ни в одну из сторон.',
                  'Ну, или когда на одном из кубов, наконец, появилась ',
                  'заветная цифра 2048. Если вы завершили игру, то ваш результат',
                  'попадает в турнирную таблицу.']
    rules_text = font.render('Правила игры', 1, pygame.Color('white'))
    screen.blit(rules_text, (250, 20))
    text_coord = 180
    for line in intro_text:
        string_rendered = font2.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    button_back.create_button(screen, (25, 25, 25, 127), 250, 650, 300, 80, 'Вернуться назад', (255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.pressed(event.pos):
                    start_screen()
                    return
        pygame.display.flip()


# турнирная таблица
def tourney_window():
    screen.blit(fon, (0, 0))
    text = font.render('Турнирная таблица', 1, pygame.Color('white'))
    screen.blit(text, (200, 20))
    button_back.create_button(screen, (25, 25, 25, 127), 250, 650, 300, 80, 'Вернуться назад', (255, 255, 255))
    with open('tourner.txt') as f:
        read_data = [(i.rstrip('/n')).split() for i in f.readlines()]
    read_data.sort(key=lambda x: int(x[-1]))
    tourney = read_data[::-1][:10]
    k = 1
    y = 120
    for i in tourney:
        s = ''
        for j in i[:-1]:
            s += str(j) + ' '
        st = f'{str(k)}. {s[:-1]} - {i[-1]}'
        string_rendered = font2.render(st, 1, pygame.Color('white'))
        screen.blit(string_rendered, (10, y))
        y += 30
        k += 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.pressed(event.pos):
                    start_screen()
                    return
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('2048')
    size = WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
    font2 = pygame.font.SysFont('cambria', 20)
    font = pygame.font.SysFont('segoeuiblack', 40)
    clock = pygame.time.Clock()
    button_back = Button()
    running = True
    while running:
        screen.fill((0, 0, 0))
        start_screen()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
