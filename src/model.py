import pywavefront
from OpenGL.GL import *
from OpenGL.GLU import *

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
        self.scaled_size = 1
        self.scale_scene = [self.scaled_size/self.max_scene_size for i in range(3)]
        self.scene_trans = [-(self.scene_box[1][i]+self.scene_box[0][i])/2 for i in range(3)]

    def render(self):
        glPushMatrix()
        glScalef(*self.scale_scene)

        for mesh in self.scene.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*self.scene.vertices[vertex_i])
            glEnd()
        glPopMatrix()