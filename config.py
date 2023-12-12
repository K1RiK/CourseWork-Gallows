class Config:
    def __init__(self, filename: str = 'config.conf'):
        self.filename = filename
        self.conf = dict()
        try:
            self.load()
            self.RES_X = int(self.conf['RES_X'])
            self.RES_Y = int(self.conf['RES_Y'])
            self.FPS = int(self.conf['FPS'])
            self.FULLSCREEN = False if self.conf['FULLSCREEN'] == 'False' else True
            self.THEME = False if self.conf['THEME'] == 'False' else True
            self.DEBUG = False if self.conf['DEBUG'] == 'False' else True
        except Exception as e:
            print(e)
            self.RES_X = 1366
            self.RES_Y = 768
            self.FPS = 50
            self.FULLSCREEN = False
            self.THEME = False
            self.DEBUG = False
            self.save()

    def load(self):
        with open(self.filename, 'r') as file:
            res = file.readlines()
        res = [r.strip() for r in res]
        for item in res:
            k, v = item.split(' = ')
            self.conf[k] = v

    def save(self):
        with open(self.filename, 'w+') as file:
            file.writelines((f"RES_X = {self.RES_X}\n",
                             f"RES_Y = {self.RES_Y}\n",
                             f"FPS = {self.FPS}\n",
                             f"FULLSCREEN = {self.FULLSCREEN}\n",
                             f"THEME = {self.THEME}\n",
                             f"DEBUG = {self.DEBUG}\n",))


config = Config()

RES_X = config.RES_X
RES_Y = config.RES_Y
FPS = config.FPS
FULLSCREEN = config.FULLSCREEN
THEME = config.THEME
DEBUG = config.DEBUG
