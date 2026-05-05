# SCC0250 - Computação Gráfica (2026) — ICMC-USP
# Model loading and vertex buffer management

from OpenGL.GL import *
import glm
import math
from PIL import Image
import random
import os

import src.state as state


def load_model_from_file(filename):
    """Loads a Wavefront OBJ file."""
    vertices = []
    texture_coords = []
    faces = []

    # abre o arquivo obj para leitura
    for line in open(filename, "r"):  # para cada linha do arquivo .obj
        if line.startswith('#'):
            continue  # ignora comentarios
        values = line.split()  # quebra a linha por espaço
        if not values:
            continue

        ### recuperando vertices
        if values[0] == 'v':
            vertices.append(values[1:4])

        ### recuperando coordenadas de textura
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        ### recuperando faces
        elif values[0] == 'f':
            face = []
            face_texture = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces

    return model


def load_texture_from_file(texture_id, img_textura):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    img = Image.open(img_textura)
    img_width = img.size[0]
    img_height = img.size[1]
    image_data = img.convert("RGBA").tobytes("raw", "RGBA", 0, -1)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_width, img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)


def gera_posicoes_arvores(raio_min, raio_max, n_arvores):
    posicoes = []
    for _ in range(n_arvores):
        angulo = random.uniform(0, 2 * math.pi)
        distancia = random.uniform(raio_min, raio_max)
        x = distancia * math.cos(angulo)
        z = distancia * math.sin(angulo)
        y = 0
        esc = random.uniform(1.2, 2.0)  # Increased scale from 0.6-1.3 to 1.2-2.0
        posicoes.append((x, y, z, esc))
    return posicoes


def _append_uv(modelo, textures_coord_list, texture_id):
    tex = modelo['texture']
    if texture_id <= 0 or texture_id > len(tex):
        textures_coord_list.append(['0.0', '0.0'])
    else:
        textures_coord_list.append(tex[texture_id - 1])


def process_faces(modelo, vertices_list, textures_coord_list, triangulate_quads=False):
    verts_src = modelo['vertices']

    for face in modelo['faces']:
        vid = face[0]
        tid = face[1] if len(face) > 1 else []
        n = len(vid)

        if triangulate_quads and n == 4:
            for a, b, c in ((0, 1, 2), (0, 2, 3)):
                vertices_list.append(verts_src[vid[a] - 1])
                _append_uv(modelo, textures_coord_list, tid[a])
                vertices_list.append(verts_src[vid[b] - 1])
                _append_uv(modelo, textures_coord_list, tid[b])
                vertices_list.append(verts_src[vid[c] - 1])
                _append_uv(modelo, textures_coord_list, tid[c])
        elif triangulate_quads and n > 4:
            # Polígonos convexos (ex.: tampos do balde): leque a partir do vértice 0
            for i in range(1, n - 1):
                vertices_list.append(verts_src[vid[0] - 1])
                _append_uv(modelo, textures_coord_list, tid[0])
                vertices_list.append(verts_src[vid[i] - 1])
                _append_uv(modelo, textures_coord_list, tid[i])
                vertices_list.append(verts_src[vid[i + 1] - 1])
                _append_uv(modelo, textures_coord_list, tid[i + 1])
        else:
            for i in range(n):
                vertices_list.append(verts_src[vid[i] - 1])
            for i in range(n):
                _append_uv(modelo, textures_coord_list, tid[i])


def carregaModelos():

    vertices_list = []
    textures_coord_list = []

    # SOLO (grama)

    modelo = load_model_from_file('models/grama/grama.obj')

    process_faces(modelo, vertices_list, textures_coord_list)

    load_texture_from_file(0, 'models/grama/grass.jpg')

    # CÉU (mesh skybox.obj + textura 2D — mesmo fluxo do antigo skydome)

    modelo = load_model_from_file('models/skybox/skybox.obj')

    process_faces(modelo, vertices_list, textures_coord_list)

    load_texture_from_file(1, 'models/skybox/skybox.png')

    # ÁRVORE (Tree.obj — casca Trank_bark + folhas polySurface1SG1; ver desenha_arvore)

    bark_tex = 'models/tree/bark_0021.jpg'
    leaf_tex = 'models/tree/DB2X2_L01.png'
    if not os.path.isfile(bark_tex):
        bark_tex = 'models/tree/tronco.jpg'
    if not os.path.isfile(leaf_tex):
        leaf_tex = 'models/tree/galho.png'
    load_texture_from_file(2, bark_tex)
    load_texture_from_file(3, leaf_tex)

    modelo = load_model_from_file('models/tree/Tree.obj')
    process_faces(modelo, vertices_list, textures_coord_list)

    load_texture_from_file(4, 'models/bench/1/Bench_4_Material_Base_Color.png')

    modelo = load_model_from_file('models/bench/Bench_4.obj')
    process_faces(modelo, vertices_list, textures_coord_list)

    load_texture_from_file(5, 'models/horse/Horse_v01.jpg')

    modelo = load_model_from_file('models/horse/10026_Horse_v01-it2.obj')
    process_faces(modelo, vertices_list, textures_coord_list, triangulate_quads=True)

    load_texture_from_file(6, 'models/wheat/10458_Wheat_Field_v1_Diffuse.jpg')

    modelo = load_model_from_file('models/wheat/10458_Wheat_Field_v1_max2010_it2.obj')
    process_faces(modelo, vertices_list, textures_coord_list, triangulate_quads=True)

    # Balde: bucket.mtl usa 4 map_Kd diferentes → 4 IDs (ver desenha_bucket em plots.py)
    load_texture_from_file(7, 'models/bucket/aiStandard1SG_basecolor.png')
    load_texture_from_file(8, 'models/bucket/aiStandard2SG_basecolor.png')
    load_texture_from_file(9, 'models/bucket/aiStandard3SG_basecolor.png')
    load_texture_from_file(10, 'models/bucket/aiStandard4SG_basecolor.png')

    modelo = load_model_from_file('models/bucket/bucket.obj')
    process_faces(modelo, vertices_list, textures_coord_list, triangulate_quads=True)

    wood_tex = 'models/logs/WoodTexture.png'
    if not os.path.isfile(wood_tex):
        wood_tex = 'models/tree/tronco.jpg'
    load_texture_from_file(11, wood_tex)

    modelo = load_model_from_file('models/logs/Wood.obj')
    process_faces(modelo, vertices_list, textures_coord_list, triangulate_quads=True)

    # COTTAGE — mat-wood-dark→tex12, mat-roof-tiles→tex13, mat-concrete→tex14, mat-wood-light→tex15
    load_texture_from_file(12, 'models/cottage/wood-dark.jpeg')
    load_texture_from_file(13, 'models/cottage/roof-tiles-color.jpeg')
    load_texture_from_file(14, 'models/cottage/concrete.jpeg')
    load_texture_from_file(15, 'models/cottage/wood-light.jpeg')

    modelo = load_model_from_file('models/cottage/small-cottage.obj')
    process_faces(modelo, vertices_list, textures_coord_list)

    # WOODEN TABLE — single material (tex 16)
    load_texture_from_file(16, 'models/wooden_table/Wooden_Table_Base_color.png')
    modelo = load_model_from_file('models/wooden_table/wooden_table.obj')
    process_faces(modelo, vertices_list, textures_coord_list)

    # WOOD CHAIR — single material (tex 17); albedo lives in wooden_table/
    load_texture_from_file(17, 'models/wooden_table/old_wooden_chair_Albedo.png')
    modelo = load_model_from_file('models/wood_chair/wood_chair.obj')
    process_faces(modelo, vertices_list, textures_coord_list)

    # CANDLE — single material (tex 18)
    load_texture_from_file(18, 'models/candle/Gravity_falls_candle_texture.png')
    modelo = load_model_from_file('models/candle/candle.obj')
    process_faces(modelo, vertices_list, textures_coord_list)

    return vertices_list, textures_coord_list
