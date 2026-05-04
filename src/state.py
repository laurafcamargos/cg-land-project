# SCC0250 - Computação Gráfica (2026) — ICMC-USP
# Global mutable state (camera, transforms, toggles)

import glm

# Window dimensions
WIDTH = 1100
HEIGHT = 800
altura = HEIGHT
largura = WIDTH

# Camera state (first-person view)
cameraPos = glm.vec3(0.0, 3.0, 15.0)
cameraFront = glm.vec3(0.0, 0.0, -1.0)
cameraUp = glm.vec3(0.0, 1.0, 0.0)

# Skybox/scene boundaries
CENTRO_SKYDOME = glm.vec3(0.0, 0.0, 0.0)
RAIO_SKYDOME = 99.0

# Interactive transformations (keyboard-controlled)
angulo_rotacao = 0
trans_x = 0
trans_z = 0

# Trigo scale (Z increases, X decreases) - max limited to horse size
trigo_scale = 0.08
TRIGO_SCALE_MIN = 0.02
TRIGO_SCALE_MAX = 0.10
TRIGO_SCALE_SPEED = 0.5  # scale units per second

# UI toggle
liga_triangulos = False

# Keyboard state
keys_pressed = set()  # currently held glfw key codes

# Mouse state (first-person camera look)
firstMouse = True
yaw = -90.0
pitch = 0.0
lastX = largura / 2
lastY = altura / 2
