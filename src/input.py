# SCC0250 - Computação Gráfica (2026) — ICMC-USP
# Keyboard and mouse input callbacks

import glfw
import glm
import math

import src.state as state


def key_event(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_P and action == glfw.PRESS:
        state.liga_triangulos = not state.liga_triangulos

    # Track currently pressed keys
    if action == glfw.PRESS:
        state.keys_pressed.add(key)
    elif action == glfw.RELEASE:
        state.keys_pressed.discard(key)


def process_camera():
    """Update camera position based on currently pressed keys."""
    cameraSpeed = 0.10
    direction = glm.normalize(state.cameraFront)

    if glfw.KEY_W in state.keys_pressed:
        newPos = state.cameraPos + cameraSpeed * direction
        if glm.distance(newPos, state.CENTRO_SKYDOME) <= state.RAIO_SKYDOME and (newPos).y >= 0.1:
            state.cameraPos += cameraSpeed * direction

    if glfw.KEY_S in state.keys_pressed:
        newPos = state.cameraPos - cameraSpeed * direction
        if glm.distance(newPos, state.CENTRO_SKYDOME) <= state.RAIO_SKYDOME and (newPos).y >= 0.1:
            state.cameraPos -= cameraSpeed * direction

    if glfw.KEY_A in state.keys_pressed:
        right_direction = glm.normalize(glm.cross(state.cameraFront, state.cameraUp)) * cameraSpeed
        if glm.distance(state.cameraPos - right_direction, state.CENTRO_SKYDOME) <= state.RAIO_SKYDOME and (state.cameraPos - cameraSpeed * direction).y >= 0:
            state.cameraPos -= right_direction

    if glfw.KEY_D in state.keys_pressed:
        right_direction = glm.normalize(glm.cross(state.cameraFront, state.cameraUp)) * cameraSpeed
        if glm.distance(state.cameraPos + right_direction, state.CENTRO_SKYDOME) <= state.RAIO_SKYDOME and (state.cameraPos - cameraSpeed * direction).y >= 0:
            state.cameraPos += right_direction

    if glfw.KEY_SPACE in state.keys_pressed:
        newPos = state.cameraPos + cameraSpeed * glm.vec3(0.0, 1.0, 0.0)
        if glm.distance(newPos, state.CENTRO_SKYDOME) <= state.RAIO_SKYDOME:
            state.cameraPos += cameraSpeed * glm.vec3(0.0, 1.0, 0.0)

    if glfw.KEY_LEFT_SHIFT in state.keys_pressed:
        newPos = state.cameraPos - cameraSpeed * glm.vec3(0.0, 1.0, 0.0)
        if glm.distance(newPos, state.CENTRO_SKYDOME) <= state.RAIO_SKYDOME and newPos.y >= 0.1:
            state.cameraPos -= cameraSpeed * glm.vec3(0.0, 1.0, 0.0)


def process_trigo_scale(delta_time):
    """Z increases scale, X decreases (clamped by state limits)."""
    if delta_time <= 0.0:
        return
    sp = state.TRIGO_SCALE_SPEED * delta_time
    if glfw.KEY_Z in state.keys_pressed:
        state.trigo_scale = min(state.TRIGO_SCALE_MAX, state.trigo_scale + sp)
    if glfw.KEY_X in state.keys_pressed:
        state.trigo_scale = max(state.TRIGO_SCALE_MIN, state.trigo_scale - sp)


def process_bench():
    """Update bench position based on arrow keys."""
    if glfw.KEY_UP in state.keys_pressed:
        state.trans_z -= 0.3
    if glfw.KEY_DOWN in state.keys_pressed:
        state.trans_z += 0.3
    if glfw.KEY_LEFT in state.keys_pressed:
        state.trans_x -= 0.3
    if glfw.KEY_RIGHT in state.keys_pressed:
        state.trans_x += 0.3


def process_horse():
    """Update horse rotation based on N/M keys."""
    if glfw.KEY_N in state.keys_pressed:
        state.angulo_rotacao -= 0.5
    if glfw.KEY_M in state.keys_pressed:
        state.angulo_rotacao += 0.5


def mouse_event(window, xpos, ypos):

    if state.firstMouse:
        state.lastX = xpos
        state.lastY = ypos
        state.firstMouse = False

    xoffset = xpos - state.lastX
    yoffset = state.lastY - ypos
    state.lastX = xpos
    state.lastY = ypos

    sensitivity = 0.35
    xoffset *= sensitivity
    yoffset *= sensitivity

    state.yaw += xoffset
    state.pitch += yoffset

    if state.pitch >= 90.0:
        state.pitch = 90.0
    if state.pitch <= -90.0:
        state.pitch = -90.0

    front = glm.vec3()
    front.x = math.cos(glm.radians(state.yaw)) * math.cos(glm.radians(state.pitch))
    front.y = math.sin(glm.radians(state.pitch))
    front.z = math.sin(glm.radians(state.yaw)) * math.cos(glm.radians(state.pitch))
    state.cameraFront = glm.normalize(front)
