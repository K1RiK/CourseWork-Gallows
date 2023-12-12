import sys
import pygame as pg
from objects import *
from locations.game import GameLocation
from locations.menu import MenuLocation
from locations.settings import SettingsLocation


class App:
    def __init__(self):
        self.config = config

        pg.init()
        pg.font.init()

        pg.display.set_caption("Виселица")
        infoObject = pg.display.Info()
        self.clock = pg.time.Clock()
        self.resolutions_count = (infoObject.current_w - infoObject.current_h + 2) // 100 - 4

        self.cursor = Cursor()
        self.location_menu = MenuLocation(self.cursor)
        self.location_settings = SettingsLocation(self.cursor, self.resolutions_count)
        self.location_game = GameLocation(self.cursor)
        self.locations = [self.location_menu, self.location_settings, self.location_game]
        self.current_location = self.location_menu

        self.window = pg.display.set_mode((RES_X, RES_Y))
        self.resize_window(RES_X, RES_Y)

        # self.FULLSCREEN = 0

    def resize_window(self, res_x: int, res_y: int):
        self.config.RES_X = res_x
        self.config.RES_Y = res_y
        self.config.save()
        if self.config.FULLSCREEN:
            self.window = pg.display.set_mode((res_x, res_y), pg.FULLSCREEN)
        else:
            pg.display.quit()
            self.window = pg.display.set_mode((res_x, res_y))
        for location in self.locations:
            location.update(res_x, res_y)

    def changeTheme(self):
        self.config.THEME = not self.config.THEME
        self.config.save()
        for location in self.locations:
            location.changeTheme(self.config.THEME)

    def main(self):
        self.cursor.update()
        self.current_location.draw(self.window)
        button = self.current_location.buttons_handler()
        if button:
            if self.current_location.name == 'menu':
                if button.name == 'Play':
                    self.current_location = self.location_game
                elif button.name == 'Settings':
                    self.current_location = self.location_settings
                elif button.name == 'Exit':
                    self.config.save()
                    sys.exit(0)
            elif self.current_location.name == 'game':
                if button.name == 'Back':
                    self.current_location = self.location_menu
            elif self.current_location.name == 'settings':
                if button.name == 'Back':
                    self.current_location = self.location_menu
                elif button.group == 'resolutions':
                    res = tuple(map(int, button.name.split('x')))
                    self.resize_window(res[0], res[1])
                elif button.name == 'Fullscreen':
                    self.config.FULLSCREEN = not self.config.FULLSCREEN
                    self.resize_window(self.config.RES_X, self.config.RES_Y)
                elif button.name == 'ChangeTheme':
                    self.changeTheme()

    def end_game(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.config.save()
                sys.exit(0)

    def start(self):
        while True:
            self.main()
            self.end_game()
            pg.display.update()
            self.clock.tick(FPS)


def main():
    app = App()
    app.start()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        with open('errors.log', 'a+', encoding='utf-8') as f:
            f.write(f"{e.text}\n")
