# Projeto 2 - Cena Externa

**SCC0250 - Computação Gráfica (2026) — ICMC-USP**

| Aluno | NUSP |
|---|---|
| Laura Fernandes Camargos | 13692334 |
| Vitor Hugo Almeida Couto | 13672787 |

An interactive 3D scene featuring a forest clearing with a cottage, outdoor objects, and a fully furnished interior. Explore the environment with camera controls and manipulate objects via keyboard.

---

## Setup

**Requirements:** Python 3.10+

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Linux / macOS
# or Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python main.py
```

---

## Controls

| Key | Action |
|-----|--------|
| W / S | Move camera forward / backward |
| A / D | Move camera left / right |
| SPACE / SHIFT | Move camera up / down |
| Mouse | Look around (rotate camera) |
| ↑ / ↓ / ← / → | Translate bench |
| N / M | Rotate horse |
| Z / X | Scale wheat up / down |
| P | Toggle wireframe mode |
| ESC | Close window |

---

## Project Structure

```
.
├── main.py                      # Entry point — window, shader setup, VBO upload, render loop
│
├── matrizes.py                  # Matrix utilities (view, projection)
│
├── src/                         # Application modules
│   ├── state.py                 # Global mutable state (camera, transforms, toggles)
│   ├── geometry.py              # Model loading + VBO management
│   ├── scene.py                 # Scene class (draw methods for each object)
│   ├── input.py                 # Keyboard/mouse callbacks
│   └── shader_s.py              # Shader loader/compiler wrapper
│
├── shaders/
│   ├── vertex_shader.vs
│   └── fragment_shader.fs
│
├── models/                      # 3D model files + textures
│   ├── grama/, skybox/, tree/, bench/
│   ├── horse/, wheat/, bucket/, logs/
│   ├── cottage/, wooden_table/, wood_chair/
│   └── candle/
│
└── requirements.txt
```

### Module Responsibilities

- **`main.py`**: Bootstrap — GLFW window, shader compilation, VBO upload, render loop
- **`src/state.py`**: Global mutable state (camera, transforms, UI toggles)
- **`src/geometry.py`**: Load OBJ models, textures; manage unified vertex buffer
- **`src/scene.py`**: Scene class with draw methods for each object
- **`src/input.py`**: GLFW keyboard/mouse callbacks
- **`src/shader_s.py`**: Shader file loader and compiler
- **`matrizes.py`**: View and projection matrix helpers

---

## Scene Composition

13 textured `.obj` models across the outdoor environment and cottage interior:

**Outdoor**
- Grass terrain and skybox
- 150 trees scattered in a ring (radius 30–95)
- Bench (interactive translation via arrow keys)
- Horse (interactive rotation via N/M)
- Wheat × 3 (interactive scale via Z/X)
- Bucket and wood logs × 3 (fixed)

**Cottage interior**
- Cottage (small-cottage.obj — wood, roof tiles, concrete materials)
- Wooden table with 4 wood chairs arranged around it
- Candle on the table

No lighting effects (per project scope).
