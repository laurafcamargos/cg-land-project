# SCC0250 - Computação Gráfica (2026) — ICMC-USP
# Scene rendering with all draw methods

from OpenGL.GL import *
import math

import src.state as state
import src.geometry as geometry
import matrizes


class Scene:
    def __init__(self, program):
        self.program = program
        self.posicoes_arvores = geometry.gera_posicoes_arvores(30, 95, 150)

    def update_matrices(self, mat_view, mat_projection):
        """Update view and projection matrices in shader"""
        loc_view = glGetUniformLocation(self.program, "view")
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

        loc_projection = glGetUniformLocation(self.program, "projection")
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)

    def desenha_grama(self):
        # rotacao
        angle = 0
        r_x = 0.0
        r_y = 0.0
        r_z = 0.0

        # translacao
        t_x = 0.0
        t_y = 0.0
        t_z = 0

        # escala
        s_x = 300
        s_y = 300
        s_z = 300

        mat_model = matrizes.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
        loc_model = glGetUniformLocation(self.program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

        glBindTexture(GL_TEXTURE_2D, 0)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)

    def desenha_skybox(self):

        angle = 0.0

        r_x = 0.0
        r_y = 1.0
        r_z = 0.0

        t_x = 0
        t_y = 0
        t_z = 0

        s_x = 100
        s_y = 100
        s_z = 100

        mat_model = matrizes.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
        loc_model = glGetUniformLocation(self.program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

        glBindTexture(GL_TEXTURE_2D, 1)
        glDrawArrays(GL_TRIANGLES, 4, 2880)

    def desenha_arvore(self, x, y, z, esc):

        # rotacao
        angle = 0
        r_x = 0.0
        r_y = 0.0
        r_z = 0.0

        # translacao
        t_x = x
        t_y = y
        t_z = z

        # escala
        s_x = esc
        s_y = esc
        s_z = esc

        mat_model = matrizes.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
        loc_model = glGetUniformLocation(self.program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 2)
        glDrawArrays(GL_TRIANGLES, 2884, 20262)
        glBindTexture(GL_TEXTURE_2D, 3)
        glDrawArrays(GL_TRIANGLES, 23146, 20910)

    def desenha_bench(self):
        angle = 115.0
        r_x = 0.0
        r_y = 1.0
        r_z = 0.0
        t_x = 4.0 + state.trans_x
        t_y = 0.0
        t_z = 15.0 + state.trans_z
        s_x = s_y = s_z = 2.75

        mat_model = matrizes.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
        loc_model = glGetUniformLocation(self.program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 4)
        glDrawArrays(GL_TRIANGLES, 44056, 4008)

    def desenha_cavalo(self):
        angle = 25.0 + state.angulo_rotacao
        r_x = 0.0
        r_y = 1.0
        r_z = 0.0
        s = 0.0022
        t_x = 22.0
        t_y = -0.000596
        t_z = 12.0
        angle_rx = -90.0

        mat_model = matrizes.model(
            angle, r_x, r_y, r_z, t_x, t_y, t_z, s, s, s, angle_rx
        )
        loc_model = glGetUniformLocation(self.program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 5)
        glDrawArrays(GL_TRIANGLES, 48064, 126768)

    def desenha_trigos(self):
        """Três instâncias do mesmo modelo de trigo perto do banco e do cavalo."""
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 6)
        loc_model = glGetUniformLocation(self.program, "model")


        s = state.trigo_scale
        t_y = 0.0
        r_x = 0.0
        r_y = 1.0
        r_z = 0.0

        angle_rx = -90.0


        instancias = [
            (18.0, 12.0, 10.5),
            (-22.0, 9.5, 9.8),
            (48.0, 13.5, 10.2),
        ]

        for angle, tx, tz in instancias:
            mat_model = matrizes.model(
                angle, r_x, r_y, r_z, tx, t_y, tz, s, s, s, angle_rx
            )
            glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
            glDrawArrays(GL_TRIANGLES, 174832, 127008)

    def desenha_bucket(self):
        """Balde com 4 texturas (bucket.mtl): um draw por faixa de material no VBO."""
        angle = 38.0
        r_x = 0.0
        r_y = 1.0
        r_z = 0.0
        s = 0.25
        t_x = 14.5
        t_y = -0.042509
        t_z = 8.0

        mat_model = matrizes.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s, s, s)
        loc_model = glGetUniformLocation(self.program, 'model')
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

        glActiveTexture(GL_TEXTURE0)
        base = 301840

        fatias = [
            (8, 7488, 0),
            (9, 4176, 7488),
            (7, 93888, 11664),
            (10, 28416, 105552),
            (8, 7488, 133968),
        ]
        for tex_id, count, offset_local in fatias:
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glDrawArrays(GL_TRIANGLES, base + offset_local, count)

    def desenha_tocos(self):
        """Tocos (Wood.obj): só madeira (tex 11). O material "Floor" do OBJ era um plano extra — não desenhamos (evita retângulo preto sob a relva)."""
        r_x = 0.0
        r_y = 1.0
        r_z = 0.0
        s = 0.45
        t_y = 0.528711

        base = 443296

        fatias_mat = [
            ('Wood', 711, 0),
            ('WoodCut', 303, 711),
            ('Wood', 711, 1014),
            ('WoodCut', 303, 1725),
            ('Wood', 711, 2028),
            ('WoodCut', 303, 2739),
            ('Wood', 711, 3042),
            ('WoodCut', 303, 3753),
            ('Wood', 711, 4056),
            ('WoodCut', 303, 4767),
            ('Wood', 711, 5076),
            ('WoodCut', 303, 5787),
        ]

        loc_model = glGetUniformLocation(self.program, 'model')
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 11)

        # (tx, tz, ângulo Y) — à volta da clareira, longe do banco/cavalo/trigo/balde
        instancias = [
            (17.2, 4.8, 42.0),
            (-15.8, 7.9, -58.0),
            (20.5, -5.5, 118.0),
        ]

        for t_x, t_z, angle in instancias:
            mat_model = matrizes.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s, s, s)
            glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
            for _nome, count, offset_local in fatias_mat:
                glDrawArrays(GL_TRIANGLES, base + offset_local, count)

    def desenha_cottage(self):
        angle = 60.0
        r_x = 0.0
        r_y = 1.0
        r_z = 0.0
        s = 1.7
        t_x = -5.0
        t_y = 0.0
        t_z = 5.0

        mat_model = matrizes.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s, s, s)
        loc_model = glGetUniformLocation(self.program, 'model')
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

        glActiveTexture(GL_TEXTURE0)
        base = 449386

        fatias = [
            (12, 0,      48),
            (13, 48,     48),
            (12, 96,   1038),
            (14, 1134,   36),
            (12, 1170,  360),
            (15, 1530,  192),
            (12, 1722,  204),
            (15, 1926,  372),
            (12, 2298,  312),
            (15, 2610,  288),
            (12, 2898,  312),
            (15, 3210,  288),
        ]
        for tex_id, local_offset, count in fatias:
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glDrawArrays(GL_TRIANGLES, base + local_offset, count)

    def desenha_mesa(self):
        mat_model = matrizes.model(60.0, 0.0, 1.0, 0.0, -5.0, 0.62, 5.0, 1.4, 1.4, 1.4)
        loc_model = glGetUniformLocation(self.program, 'model')
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 16)
        glDrawArrays(GL_TRIANGLES, 452884, 492)

    def desenha_cadeiras(self):
        loc_model = glGetUniformLocation(self.program, 'model')
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 17)

        instancias = [
            (330.0, -4.0, 0.7,  3.5),
            (150.0, -6.0, 0.7,  6.5),
            (240.0, -3.5, 0.7,  6.0),
            (60.0, -6.5, 0.7,  4.0),
        ]
        for angle, tx, ty, tz in instancias:
            mat_model = matrizes.model(angle, 0.0, 1.0, 0.0, tx, ty, tz, 1.0, 1.0, 1.0)
            glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
            glDrawArrays(GL_TRIANGLES, 453376, 2676)

    def desenha_vela(self):
        mat_model = matrizes.model(60.0, 0.0, 1.0, 0.0, -5.0, 1.97, 5.0, 10.0, 10.0, 10.0)
        loc_model = glGetUniformLocation(self.program, 'model')
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 18)
        glDrawArrays(GL_TRIANGLES, 456052, 1512)

    def draw_all(self):
        """Execute all draw calls in order"""
        self.desenha_grama()
        self.desenha_skybox()
        self.desenha_bench()
        self.desenha_cavalo()
        self.desenha_trigos()
        self.desenha_bucket()
        self.desenha_tocos()
        self.desenha_cottage()
        self.desenha_mesa()
        self.desenha_cadeiras()
        self.desenha_vela()
        for x, y, z, esc in self.posicoes_arvores:
            self.desenha_arvore(x, y, z, esc)
