# SCC0250 - Computação Gráfica (2026) — ICMC-USP
# Laura Fernandes Camargos - 13692334
# Vitor Hugo Almeida Couto - 13672787

import glfw
from OpenGL.GL import *
import numpy as np
import ctypes
import os
from PIL import Image

from src.shader_s import Shader
from src import state
from src import geometry
from src import input as inp
from src.scene import Scene
import matrizes


# Window initialization
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

window = glfw.create_window(state.WIDTH, state.HEIGHT, "Projeto 2 - Cena Externa", None, None)
if not window:
    glfw.terminate()
    raise RuntimeError("Failed to create GLFW window")

glfw.make_context_current(window)

# Shaders
ourShader = Shader("shaders/vertex_shader.vs", "shaders/fragment_shader.fs")
ourShader.use()
program = ourShader.getProgram()

# Create fallback skybox texture if missing
sky_tex = 'models/skybox/skybox.png'
if not os.path.isfile(sky_tex):
    os.makedirs(os.path.dirname(sky_tex), exist_ok=True)
    img = Image.new("RGBA", (1024, 768), (135, 206, 235, 255))
    img.save(sky_tex)

# Create fallback bucket textures if missing
bucket_dir = 'models/bucket'
for png_name in (
    'aiStandard1SG_basecolor.png',
    'aiStandard2SG_basecolor.png',
    'aiStandard3SG_basecolor.png',
    'aiStandard4SG_basecolor.png',
):
    p = os.path.join(bucket_dir, png_name)
    if not os.path.isfile(p):
        os.makedirs(bucket_dir, exist_ok=True)
        Image.new('RGB', (64, 64), (140, 130, 120)).save(p)

# Load models and textures
textures = glGenTextures(12)
vertices_list, textures_coord_list = geometry.carregaModelos()

# Setup vertex position VBO
vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
vertices['position'] = vertices_list

vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

loc_position = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc_position)
glVertexAttribPointer(loc_position, 3, GL_FLOAT, False, vertices.strides[0], ctypes.c_void_p(0))

# Setup texture coordinate VBO
textures_buf = np.zeros(len(textures_coord_list), [("position", np.float32, 2)])
textures_buf['position'] = textures_coord_list

vbo_tex = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo_tex)
glBufferData(GL_ARRAY_BUFFER, textures_buf.nbytes, textures_buf, GL_STATIC_DRAW)

loc_texture_coord = glGetAttribLocation(program, "texture_coord")
glEnableVertexAttribArray(loc_texture_coord)
glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, textures_buf.strides[0], ctypes.c_void_p(0))

# Scene
scene = Scene(program)

# Input callbacks
glfw.set_key_callback(window, inp.key_event)
glfw.set_cursor_pos_callback(window, inp.mouse_event)

# OpenGL state setup
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_LINE_SMOOTH)
glEnable(GL_TEXTURE_2D)
glEnable(GL_DEPTH_TEST)

glfw.show_window(window)
glfw.set_cursor_pos(window, state.lastX, state.lastY)

# Render loop timing
last_frame = 0.0

# Render loop
while not glfw.window_should_close(window):
    now = glfw.get_time()
    delta_time = now - last_frame
    last_frame = now

    if state.liga_triangulos:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glfw.poll_events()

    # Update input (process held keys)
    inp.process_camera()
    inp.process_trigo_scale(delta_time)
    inp.process_bench()
    inp.process_horse()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)

    glUseProgram(program)

    # Update matrices
    mat_view = matrizes.view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

    mat_projection = matrizes.projection(state.altura, state.largura)
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)

    # Draw scene
    scene.draw_all()

    glfw.swap_buffers(window)

glfw.terminate()
