import math
import glm
import numpy as np

import src.state as state 

def model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, angle_rx=0.0):
    
    angle = math.radians(angle)
    rx = math.radians(angle_rx)
    
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade
       
    # aplicando translacao (terceira operação a ser executada)
    matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))    
    
    # aplicando rotacao (segunda operação a ser executada)
    if angle!=0:
        matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z))

    # rotação extra em X (ex.: modelo Z-up → cena Y-up), entre R_y e escala
    if abs(rx) > 1e-9:
        matrix_transform = glm.rotate(matrix_transform, rx, glm.vec3(1.0, 0.0, 0.0))
    
    # aplicando escala (primeira operação a ser executada)
    matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))
    
    matrix_transform = np.array(matrix_transform)
    
    return matrix_transform

def view():
    mat_view = glm.lookAt(state.cameraPos, state.cameraPos + state.cameraFront, state.cameraUp);
    mat_view = np.array(mat_view)
    return mat_view

def projection(altura, largura):
    mat_projection = glm.perspective(glm.radians(45.0), largura/altura, 0.1, 1000.0)
    mat_projection = np.array(mat_projection)
    return mat_projection