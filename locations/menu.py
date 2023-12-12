from objects import *


class MenuLocation(Location):
    def __init__(self, cursor):
        '''Класс локации главного меню'''
        super().__init__('menu', cursor)

        self.buttons_width = 256
        self.buttons_height = 100

        self.buttons = \
            (Button('Play', 0, 0, self.buttons_width, self.buttons_height),
             Button('Settings', 0, 0, self.buttons_width, self.buttons_height,
                    text_correction=(-45, -4)),
             Button('Exit', 0, 0, self.buttons_width, self.buttons_height))

        self.update()

    def update(self, res_x: int = RES_X, res_y: int = RES_Y):
        buttons_shift = 128
        buttons_start_x = res_x / 2 - self.buttons_width / 2
        buttons_start_y = res_y / 2 - (self.buttons_height * 3) / 2

        for i, button in enumerate(self.buttons):
            button.set_pos(buttons_start_x, buttons_start_y + i*buttons_shift)

    def changeTheme(self, theme: int):
        super().changeTheme(theme)
        for button in self.buttons:
            button.changeTheme(self.theme)

    def draw(self, window):
        '''Метод отрисовки локации главного меню'''
        super().draw(window)
        for button in self.buttons:
            button.draw(window, 0)

    def buttons_handler(self):
        for button in self.buttons:
            if button.isPressed(self.cursor):
                return button
