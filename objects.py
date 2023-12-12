from baseObjects import *


class CheckButton(Button):
    def __init__(self, name: str, x: int, y: int, width: int, height: int,
                 rgb_color: tuple = (25, 25, 25), text_correction: tuple = (0, 0),
                 font_size: int = 24, group: str = ''):
        '''Класс всех графических кнопок на экране'''
        super().__init__(name, x, y, width, height, rgb_color,
                         text_correction, font_size, group)
        self.textdraw = Textdraw((self.x + 15 + width + text_correction[0],
                                  self.y + height / 3 + text_correction[1]),
                                 self.name, font_size=font_size)
        self.isActive = 0
        self.changeTheme(self.theme)

    def draw(self, window, fill: int = 0):
        '''Метод отрисовки кнопки'''
        super().draw(window, fill)
        pg.draw.rect(window, self.border_color, self.rect, 5)
        if self.isActive:
            pg.draw.rect(window, self.border_color, (self.x + 10, self.y + 10, self.width - 20, self.height - 20), 0)
        self.textdraw.show(window)

    def set_pos(self, x: int, y: int):
        super().set_pos(x, y)
        self.textdraw.set_pos(self.x + 15 + self.width + self.text_correction[0],
                              self.y + self.height / 3 + self.text_correction[1])

    def changeTheme(self, theme: int):
        super().changeTheme(theme)
        self.textdraw.changeTheme(theme)
        if self.theme:
            self.border_color = (50, 50, 50)
        else:
            self.border_color = (200, 200, 200)

    def isPressed(self, cursor):
        isCursorOnButton = self.rect.collidepoint(cursor.get_pos())
        if isCursorOnButton and not self.isChanged:
            self.color = self.hover_color
            self.isChanged = 1
        elif not isCursorOnButton and self.isChanged:
            self.color = self.rgb_color
            self.isChanged = 0
        if isCursorOnButton and cursor.get_clicked():
            self.isActive = not self.isActive
            return 1
        return 0


class ControlBar(Entity):
    def __init__(self):
        pass

    def draw(self):
        pass


class Keyboard:
    def __init__(self, cursor):
        self.cursor = cursor
        self.keys = ["ЙЦУКЕНГШЩЗХЪ", "ФЫВАПРОЛДЖЭ", "ЯЧСМИТЬБЮ"]
        self.buttons_width = 64
        self.buttons_height = 64
        self.buttons = []
        for i, line in enumerate(self.keys):
            for j, k in enumerate(line):
                self.buttons.append(
                    Button(k, RES_X / 2 - (len(line) / 2 - j) * (self.buttons_width * 1.1),
                           RES_Y - (4 - i) * (self.buttons_height * 1.1),
                           self.buttons_width, self.buttons_height, font_size=36))

    def draw(self, window):
        for button in self.buttons:
            if not button.locked:
                button.draw(window, 0)

    def update(self, res_x: int, res_y: int):
        k = 0
        for i, line in enumerate(self.keys):
            for j in range(len(line)):
                self.buttons[k].set_pos(res_x / 2 - (len(line) / 2 - j) * (self.buttons_width * 1.1),
                                        res_y - (4 - i) * (self.buttons_height * 1.1))
                k += 1

    def changeTheme(self, theme: int):
        for button in self.buttons:
            button.changeTheme(theme)

    def buttons_handler(self):
        for button in self.buttons:
            if not button.locked and button.isPressed(self.cursor):
                return button
