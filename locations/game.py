from objects import *


class GameLocation(Location):
    def __init__(self, cursor):
        '''Основная игровая локация'''
        super().__init__('game', cursor)
        self.buttons_width = 128
        self.buttons_height = 64
        self.buttons = [Button('Back', 0, 0, self.buttons_width, self.buttons_height,
                               text_correction=(0, 0), font_size=42)]
        self.res_x = RES_X
        self.res_y = RES_Y
        self.reset()

    def reset(self):
        self.keyboard = Keyboard(self.cursor)
        self.word = RandomWord().word
        self.errors_count = 0
        self.draw_word = ["_ " for i in range(len(self.word))]
        self.word_textdraw = Textdraw((RES_X / 2 - len(self.word) / 2 * 36, RES_Y - 4 * (self.buttons_height * 1.5)),
                                      ''.join(self.draw_word), font_size=64)
        self.update(self.res_x, self.res_y)

    def update(self, res_x: int, res_y: int):
        self.res_x = res_x
        self.res_y = res_y
        self.word_textdraw.set_pos(res_x / 2 - len(self.word) / 2 * 36, res_y - 4 * (self.buttons_height * 1.5))
        self.keyboard.update(res_x, res_y)

    def changeTheme(self, theme: int):
        super().changeTheme(theme)
        self.keyboard.changeTheme(theme)
        for button in self.buttons:
            button.changeTheme(self.theme)

    def draw(self, window):
        super().draw(window)
        self.keyboard.draw(window)
        self.word_textdraw.show(window)
        for button in self.buttons:
            if not button.locked:
                button.draw(window, 0)

    def buttons_handler(self):
        self.pressed_key = self.keyboard.buttons_handler()
        if self.pressed_key:
            self.pressed_key.locked = 1
            # self.keyboard.buttons.remove(self.pressed_key)
            if self.pressed_key.name in self.word:
                for i, k in enumerate(self.word):
                    if k == self.pressed_key.name:
                        self.draw_word[i] = f"{k} "
                self.word_textdraw.text = ''.join(self.draw_word)
                if ''.join([k.strip() for k in self.draw_word]) == self.word:
                    print("Вы выйграли")
                    self.reset()
            else:
                self.errors_count += 1
                if self.errors_count == 9:
                    print("Вы проиграли")
                    self.reset()
        for button in self.buttons:
            if button.isPressed(self.cursor):
                return button
