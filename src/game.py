import pygame as pg
import pygame.freetype
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
# import datetimegame
import numpy as np



# Interface for a custom 3d object to render
class Model:
    def __init__(self, src: str):
        print(f'loading: {src}...')

        self.scene = pywavefront.Wavefront(src, collect_faces=True)
        self.scene_box = self.scene.vertices[0], self.scene.vertices[0]
        for vertex in self.scene.vertices:
            min_v = [min(self.scene_box[0][i], vertex[i]) for i in range(3)]
            max_v = [max(self.scene_box[0][i], vertex[i]) for i in range(3)]
            self.scene_box = (min_v, max_v)
        
        self.scene_size = [self.scene_box[1][i] for i in range(3)]
        self.max_scene_size = max(self.scene_size)
        self.scaled_size = 2
        self.scale_scene = [self.scaled_size/self.max_scene_size for i in range(3)]
        self.scene_trans = [-(self.scene_box[1][i]+self.scene_box[0][i])/2 for i in range(3)]
        self.fast_verts = np.array(self.scene.vertices)
        self.translation_vector = [0, 0, 0]
        self.translation_factor = 0
        self.dirty = False


    def scale(self, factor: int):
        self.scaled_size = factor
        return self
    
    def translate(self, vector: list, factor: int):
        self.translation_factor = factor
        self.translation_vector = vector

    def render(self):
        glPushMatrix()
        glScalef(*self.scale_scene)

        for mesh in self.scene.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vert in face:
                    glVertex3f(*self.scene.vertices[vert])

                # glVertex3f(*self.scene.vertices[face[0]])
                # glVertex3f(*self.scene.vertices[face[1]])
                # glVertex3f(*self.scene.vertices[face[2]])
            glEnd()
        glPopMatrix()


def renderModel(model: Model):
    glPushMatrix()
    glScalef(*model.scale_scene)

    for mesh in model.scene.mesh_list:
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vert in face:
                glVertex3f(*model.scene.vertices[vert])

            # glVertex3f(*self.scene.vertices[face[0]])
            # glVertex3f(*self.scene.vertices[face[1]])
            # glVertex3f(*self.scene.vertices[face[2]])
        glEnd()
    glPopMatrix()
    model.dirty = not model.dirty

class App:
    def __init__(self):
        # Init pygame
        pg.init()
        self.display = (1080, 640)
        self.screen = pg.display.set_mode(self.display, pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        # Init opengl
        glClearColor(0.0, 0.2, 0.3, 1.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        gluPerspective(45, (self.display[0]/self.display[1]), 0.1, 50.0)
        glTranslatef(0.0,0.0, -5)
        self.game_font = pg.font.SysFont('arial', 12)

        # self.cube = Model('assets/cube.obj')
        
        self.models = [
            Model('assets/teapot.obj'),
            Model('assets/cube.obj')
        ]

        self.mainloop()

    def draw_text(self, text, x, y):
        textSurface = self.game_font.render(text, True, (227, 164, 48, 255)).convert_alpha()
        # textSurface = self.game_font.render(text, True, (255, 255, 66, 255)).convert_alpha()
        textData = pg.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x, y)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


    def mainloop(self):
        running = True
        while (running):
            dt = self.clock.tick()
            # Check for events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            
            # refresh screen
            # glRotatef(1 * dt / 5, 3 * dt / 5, 1* dt / 5, 1 * dt / 5)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            # cube = Cube()
            # cube.render()
            for model in self.models:
                # renderModel(model)
                model.render()
            # self.model.render()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

            self.draw_text(f'{self.clock.get_fps()}', 20, 20)

            pg.display.flip()
            # pg.time.wait(10)

            # # timing
        self.quit()

    def quit(self):
        pg.quit()


if __name__ == '__main__':
    my_app = App()
