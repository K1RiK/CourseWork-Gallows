import pygame as pg
from random import choice
from config import *


class Entity:
    def __init__(self, x: int, y: int, width: int, height: int):
        '''Класс всех сущностей с которыми можно взаимодействовать или видеть'''
        self.x = x  # Позиция по x
        self.y = y  # Позиция по y
        self.width = width  # Ширина
        self.height = height  # Высота
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)  # Прямоугольник для взаимодействия

    def draw(self, window, rgb_color: tuple = (0, 0, 0), fill: int = 0):
        '''Метод отрисовки сущности'''
        pg.draw.rect(window, rgb_color, self.rect, fill)  # Отрисовка прямоугольника если fill >= 0,
        if DEBUG:  # Если включен режим отладки
            pg.draw.rect(window, (0, 200, 0), self.rect, 5)

    def set_pos(self, x: int, y: int):
        '''Метод установки координат для сущности'''
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)


class Textdraw:
    def __init__(self, position: tuple, text: str, font=None, font_size: int = 36, color: tuple = (255, 255, 255)):
        '''Класс текста на экране'''
        self.text = text  # Текст надписи
        self.font = pg.font.Font(font, font_size)  # Шрифт и размер надписи
        self.color = color  # Цвет надписи
        self.position = position  # Позиция надписи (x, y)
        self.theme = THEME

    def show(self, window):
        '''Метод отрисовки текста'''
        window.blit(self.font.render(self.text, True, self.color), self.position)  # Отрисовка надписи на экране

    def changeTheme(self, theme: int):
        '''Метод смены цвета и темы'''
        self.theme = theme
        if self.theme:
            self.color = (0, 0, 0)
        else:
            self.color = (255, 255, 255)

    def set_pos(self, x: int, y: int):
        '''Метод установки координат для текста'''
        self.position = (x, y)


class Cursor:
    def __init__(self):
        '''Класс курсора мыши для взаимодействий'''
        self.update()

    def update(self):
        '''Метод обновления координат и состояния клавиш мыши'''
        self.x = pg.mouse.get_pos()[0]  # Позиция курсора по X
        self.y = pg.mouse.get_pos()[1]  # Позиция курсора по Y
        self.click = pg.mouse.get_pressed()  # Состояние клавиш мыши (ЛКМ, ПКМ, СКМ)
        # print(self.x, self.y)

    def get_pos(self):
        '''Метод возвращает позицию курсора мыши по X и Y'''
        return self.x, self.y

    def get_pressed(self):
        '''Метод возвращает значение клавиш мыши (1 - нажата, 0 - не нажата)'''
        return self.click

    def get_clicked(self):
        '''Метод возвращает 1 в момент отжатия ЛКМ иначе 0'''
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:  # Если кнопка мыши нажата и отжата
                return 1
        return 0


class Location:
    def __init__(self, name: str, cursor):
        '''Класс всех локаций между которыми можно переключаться (прим. Меню, Настройки и т.д.)'''
        self.name = name  # Название локации
        self.cursor = cursor  # Класс курсора для проверки коллизий с сущностями
        self.theme = THEME
        self.background_color = (180, 180, 180) if self.theme else (75, 75, 75)

    def draw(self, window):
        '''Метод отрисовки локации'''
        window.fill(self.background_color)  # Заливка фона всего окна

    def changeTheme(self, theme: int):
        '''Метод смены цвета и темы'''
        self.theme = theme
        if self.theme:
            self.background_color = (180, 180, 180)
        else:
            self.background_color = (75, 75, 75)


class RandomWord:
    def __init__(self):
        '''Класс выбираюий случайное слово из списка'''
        with open('words.txt', 'r', encoding='utf-8') as f:
            words = f.readlines()
        words = [word.strip().upper() for word in words]
        self.word = choice(words)


class Button(Entity):
    def __init__(self, name: str, x: int, y: int, width: int, height: int,
                 rgb_color: tuple = (25, 25, 25), text_correction: tuple = (0, 0),
                 font_size: int = 64, group: str = ''):
        '''Класс всех кнопок на экране'''
        super().__init__(x, y, width, height)
        self.name = name
        self.group = group
        self.text_correction = text_correction
        self.textdraw = Textdraw((self.x + width / 3 + text_correction[0],
                                  self.y + height / 3 + text_correction[1]),
                                 self.name, font_size=font_size)
        self.theme = THEME
        self.changeTheme(self.theme)
        self.isChanged = 0
        self.locked = 0

    def draw(self, window, fill: int = 0):
        '''Метод отрисовки кнопки'''
        super().draw(window, self.color, fill)
        self.textdraw.show(window)

    def changeTheme(self, theme):
        '''Метод смены цвета и темы'''
        self.theme = theme
        self.textdraw.changeTheme(theme)
        if self.theme:
            self.rgb_color = (200, 200, 200)
            self.hover_color = (150, 150, 150)
        else:
            self.rgb_color = (25, 25, 25)
            self.hover_color = (100, 100, 100)
        self.color = self.rgb_color

    def set_pos(self, x: int, y: int):
        '''Метод установки координат для кнопки'''
        super().set_pos(x, y)
        self.textdraw.set_pos(self.x + self.width / 3 + self.text_correction[0],
                              self.y + self.height / 3 + self.text_correction[1])

    def isPressed(self, cursor):
        '''Метод проверяет коллизию курсора с кнопкой и
           была ли нажата кнопка и возвращает 1 если была нажата иначе 0'''
        isCursorOnButton = self.rect.collidepoint(cursor.get_pos())
        if isCursorOnButton and not self.isChanged:
            self.color = self.hover_color
            self.isChanged = 1
        elif not isCursorOnButton and self.isChanged:
            self.color = self.rgb_color
            self.isChanged = 0
        if isCursorOnButton and cursor.get_clicked():
            return 1
        return 0
