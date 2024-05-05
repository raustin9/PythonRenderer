import pygame as pg
import pygame.freetype
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Cube:
    def __init__(self):
        self.vertices = (
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, -1, 1),
            (-1, 1, 1)
        )

        self.edges = (
            (0,1),
            (0,3),
            (0,4),
            (2,1),
            (2,3),
            (2,7),
            (6,3),
            (6,4),
            (6,7),
            (5,1),
            (5,4),
            (5,7)
        )

    def render(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()


class App:
    def __init__(self):
        # Init pygame
        pg.init()
        self.display = (640, 480)
        self.screen = pg.display.set_mode(self.display, pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        # Init opengl
        glClearColor(1.0, 0.2, 0.2, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        gluPerspective(45, (self.display[0]/self.display[1]), 0.1, 50.0)
        glTranslatef(0.0,0.0, -5)
        self.game_font = pg.font.SysFont('arial', 12)
        self.mainloop()

    def draw_text(self, text, x, y):
        textSurface = self.game_font.render(text, True, (255, 255, 66, 255)).convert_alpha()
        # textSurface = self.game_font.render(text, True, (255, 255, 66, 255)).convert_alpha()
        textData = pg.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x, y)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


    def mainloop(self):
        running = True
        while (running):
            # Check for events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            
            # refresh screen
            glRotatef(1, 3, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            cube = Cube()
            cube.render()

            self.draw_text(f'{self.clock.get_fps()}', 20, 20)

            pg.display.flip()
            pg.time.wait(10)
            # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # pg.display.flip()

            # # timing
            self.clock.tick()
        self.quit()

    def quit(self):
        pg.quit()


if __name__ == '__main__':
    my_app = App()