# SCC0250 - Computação Gráfica (2026) — ICMC-USP
# Shader loader and compiler wrapper

from OpenGL.GL import *
import OpenGL.GL.shaders


class Shader:
    """Loads, compiles, and manages a shader program from external files."""

    def __init__(self, vertex_path, fragment_path):
        """
        Load and compile vertex and fragment shaders from files.

        Args:
            vertex_path: Path to .vs (vertex shader) file
            fragment_path: Path to .fs (fragment shader) file
        """
        # Read shader source from files
        with open(vertex_path, 'r') as f:
            vertex_code = f.read()

        with open(fragment_path, 'r') as f:
            fragment_code = f.read()

        # Request a program and shader slots from GPU
        self.program = glCreateProgram()
        vertex = glCreateShader(GL_VERTEX_SHADER)
        fragment = glCreateShader(GL_FRAGMENT_SHADER)

        # Set shaders source
        glShaderSource(vertex, vertex_code)
        glShaderSource(fragment, fragment_code)

        # Compile shaders
        glCompileShader(vertex)
        if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(vertex).decode()
            print(error)
            raise RuntimeError("Erro de compilacao do Vertex Shader")

        glCompileShader(fragment)
        if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(fragment).decode()
            print(error)
            raise RuntimeError("Erro de compilacao do Fragment Shader")

        # Attach shader objects to the program
        glAttachShader(self.program, vertex)
        glAttachShader(self.program, fragment)

        # Build program
        glLinkProgram(self.program)
        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            print(glGetProgramInfoLog(self.program))
            raise RuntimeError('Linking error')

        # Make program the default program
        glUseProgram(self.program)

        loc_sampler = glGetUniformLocation(self.program, "samplerTexture")
        if loc_sampler >= 0:
            glUniform1i(loc_sampler, 0)

    def use(self):
        """Activate this shader program."""
        glUseProgram(self.program)

    def getProgram(self):
        """Return the OpenGL program ID."""
        return self.program
