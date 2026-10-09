import pygame
import random

# Importar la clase Rocket del archivo anterior
from rocket import Rocket

# ----------------------------------------------------------------------
# MOCK TEMPORAL DE DNA (Para que pruebes tus gráficos antes de que
# tu compañero termine el motor genético real)
# ----------------------------------------------------------------------
class MockDNA:
    def __init__(self, lifespan):
        self.genes = []
        for _ in range(lifespan):
            # Fuerza aleatoria en 2D con magnitud controlada
            v = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            if v.length_squared() > 0:
                v.scale_to_length(0.3)
            self.genes.append(v)

# ----------------------------------------------------------------------
# CONFIGURACIÓN DEL ENTORNO
# ----------------------------------------------------------------------
WIDTH, HEIGHT = 800, 600
LIFESPAN = 300       # Frames que dura cada generación
POP_SIZE = 50        # Cantidad de cohetes

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Rockets - Algoritmo Genético")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 16)
big_font = pygame.font.SysFont("Consolas", 22, bold=True)

# Elementos del entorno
TARGET_POS = pygame.math.Vector2(WIDTH // 2, 60)
TARGET_RADIUS = 18
START_POS = pygame.math.Vector2(WIDTH // 2, HEIGHT - 50)
SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)

# Obstáculos (Rectángulos)
OBSTACLES = [
    pygame.Rect(WIDTH // 4, HEIGHT // 2 - 10, WIDTH // 2, 20),
    pygame.Rect(WIDTH // 6, HEIGHT // 4, 120, 15),
    pygame.Rect(WIDTH - WIDTH // 6 - 120, HEIGHT // 4, 120, 15)
]

# Inicializar población de prueba
rockets = [Rocket(START_POS.x, START_POS.y, MockDNA(LIFESPAN)) for _ in range(POP_SIZE)]

# Variables de control
generation = 1
frame_count = 0
fps_target = 60
paused = False
running = True

# ----------------------------------------------------------------------
# BUCLE PRINCIPAL DE LA SIMULACIÓN
# ----------------------------------------------------------------------
while running:
    # 1. Procesamiento de Eventos y Teclado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_UP:
                fps_target = min(fps_target + 60, 480)   # Acelerar simulación
            elif event.key == pygame.K_DOWN:
                fps_target = max(fps_target - 60, 60)    # Velocidad normal
            elif event.key == pygame.K_r:
                # Reinicio manual de generación
                frame_count = 0
                rockets = [Rocket(START_POS.x, START_POS.y, MockDNA(LIFESPAN)) for _ in range(POP_SIZE)]

    # 2. Actualización de Física (si no está en pausa)
    if not paused:
        all_stopped = True
        for r in rockets:
            r.update(frame_count, TARGET_POS, TARGET_RADIUS, OBSTACLES, SCREEN_RECT)
            if not r.crashed and not r.completed:
                all_stopped = False

        frame_count += 1

        # Fin del ciclo de vida de la generación
        if frame_count >= LIFESPAN or all_stopped:
            # AQUÍ TU COMPAÑERO CONECTARÁ SU MÉTODO:
            # rockets = poblacion.evolucionar()
            
            # Reemplazo temporal para mantener el ciclo corriendo:
            frame_count = 0
            generation += 1
            rockets = [Rocket(START_POS.x, START_POS.y, MockDNA(LIFESPAN)) for _ in range(POP_SIZE)]

    # 3. Renderizado
    screen.fill((20, 24, 35))  # Fondo oscuro elegante

    # Dibujar Meta
    pygame.draw.circle(screen, (50, 220, 90), (int(TARGET_POS.x), int(TARGET_POS.y)), TARGET_RADIUS)
    pygame.draw.circle(screen, (200, 255, 200), (int(TARGET_POS.x), int(TARGET_POS.y)), TARGET_RADIUS, 3)

    # Dibujar Obstáculos
    for obs in OBSTACLES:
        pygame.draw.rect(screen, (160, 40, 60), obs, border_radius=4)
        pygame.draw.rect(screen, (220, 80, 100), obs, width=2, border_radius=4)

    # Dibujar Cohetes
    for r in rockets:
        r.draw(screen)

    # 4. Renderizado del HUD (Interfaz en Pantalla)
    completed_count = sum(1 for r in rockets if r.completed)
    crashed_count = sum(1 for r in rockets if r.crashed)

    ui_lines = [
        f"Generación: {generation}",
        f"Frame: {frame_count}/{LIFESPAN}",
        f"Completados: {completed_count}/{POP_SIZE}",
        f"Estrellados: {crashed_count}/{POP_SIZE}",
        f"Velocidad: {fps_target} FPS (Flechas Arriba/Abajo)",
        "Espacio: Pausar | R: Reiniciar"
    ]

    # Panel lateral de fondo para el texto
    panel_rect = pygame.Rect(10, 10, 310, len(ui_lines) * 22 + 10)
    pygame.draw.rect(screen, (10, 12, 18, 200), panel_rect, border_radius=6)
    pygame.draw.rect(screen, (60, 70, 90), panel_rect, width=1, border_radius=6)

    for i, line in enumerate(ui_lines):
        txt_surf = font.render(line, True, (230, 230, 240))
        screen.blit(txt_surf, (20, 16 + i * 22))

    if paused:
        pause_surf = big_font.render("[SIMULACIÓN PAUSADA]", True, (255, 200, 50))
        screen.blit(pause_surf, (WIDTH // 2 - pause_surf.get_width() // 2, HEIGHT - 30))

    pygame.display.flip()
    clock.tick(fps_target)

pygame.quit()