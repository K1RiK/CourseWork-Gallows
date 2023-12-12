from objects import *


class SettingsLocation(Location):
    def __init__(self, cursor, resolutions_count: int = 4):
        '''Класс локации настроек игры'''
        super().__init__('settings', cursor)
        # self.resolutions_count = resolutions_count
        self.inbackgruond_color = (80, 80, 80)
        self.select_section = ''
        self.section_buttons = ()

        self.buttons_width = 128
        self.buttons_height = 50

        self.buttons = \
            (Button('Back', 0, 0, self.buttons_width, self.buttons_height,
                    text_correction=(-4, -4), font_size=36),
             Button('Sound', 0, 0, self.buttons_width, self.buttons_height,
                    text_correction=(-16, -4), font_size=36),
             Button('Graphics', 0, 0, self.buttons_width, self.buttons_height,
                    text_correction=(-30, -3), font_size=36))

        resolutions = ('1920x1080', '1600x900', '1366x768', '1280x720')[-1:-resolutions_count - 1:-1]
        self.graphics_buttons =\
            [Button(res, 0, 0, self.buttons_width, self.buttons_height,
                    text_correction=(-30, -4), font_size=30, group='resolutions') for i, res in enumerate(resolutions)]
        self.checkButton = CheckButton('Fullscreen', 0, 0, 50, 50)
        self.checkButton.isActive = FULLSCREEN
        self.themeButton = CheckButton('ChangeTheme', 0, 0, 50, 50)
        self.themeButton.isActive = THEME
        self.graphics_buttons.append(self.checkButton)
        self.graphics_buttons.append(self.themeButton)
        self.graphics_buttons = tuple(self.graphics_buttons)
        self.all_buttons = self.buttons + self.graphics_buttons

        self.update()

    def update(self, res_x: int = RES_X, res_y: int = RES_Y):
        buttons_shift = 64
        buttons_start_x = res_x / 16 + self.buttons_width / 4
        buttons_start_y = res_y / 9 + self.buttons_height / 2

        self.backgruond_rect = pg.Rect(res_x / 16, res_y / 9, res_x - res_x / 8, res_y - res_y / 4.5)
        self.inbackgruond_rect = pg.Rect(res_x / 16 + self.buttons_width + self.buttons_width / 2,
                                         buttons_start_y, res_x - res_x / 8 - self.buttons_width * 2,
                                         res_y - res_y / 4.5 - buttons_shift)

        for i, button in enumerate(self.buttons):
            button.set_pos(buttons_start_x, buttons_start_y + i*buttons_shift)

        graphics_buttons_start_x = res_x / 16 + self.buttons_width * 2
        graphics_buttons_start_y = res_y / 9 + self.buttons_height

        for i, button in enumerate(self.graphics_buttons):
            if button.group == 'resolutions':
                button.set_pos(graphics_buttons_start_x, graphics_buttons_start_y + i*buttons_shift)
            elif button.name == 'Fullscreen':
                button.set_pos(graphics_buttons_start_x + 150, graphics_buttons_start_y)
            elif button.name == 'ChangeTheme':
                button.set_pos(graphics_buttons_start_x + 150, graphics_buttons_start_y + buttons_shift)

        if self.select_section != '':
            if self.select_section == 'sound':
                self.draw_sound()
            elif self.select_section == 'graphics':
                self.draw_graphics()

    def changeTheme(self, theme: int):
        super().changeTheme(theme)
        for button in self.all_buttons:
            button.changeTheme(self.theme)

    def draw(self, window):
        '''Метод отрисовки локации главного меню'''
        super().draw(window)
        if self.theme:
            pg.draw.rect(window, (220, 220, 220), self.backgruond_rect, 0)
        else:
            pg.draw.rect(window, (180, 180, 180), self.backgruond_rect, 0)
        pg.draw.rect(window, self.inbackgruond_color, self.inbackgruond_rect, 0)
        for button in self.buttons + self.section_buttons:
            button.draw(window, 0)

    def draw_sound(self):
        self.inbackgruond_color = (0, 0, 100)
        self.section_buttons = ()

    def draw_graphics(self):
        self.inbackgruond_color = (100, 70, 70)
        self.section_buttons = self.graphics_buttons

    def buttons_handler(self):
        for button in self.buttons + self.section_buttons:
            if button.isPressed(self.cursor):
                if button.name == "Sound":
                    self.draw_sound()
                elif button.name == "Graphics":
                    self.draw_graphics()
                return button
