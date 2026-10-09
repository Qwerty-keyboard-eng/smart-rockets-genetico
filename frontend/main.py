import sys
from pathlib import Path
import pygame
import math
import random

# 1. Le enseñamos a Python a mirar la carpeta raíz del proyecto y la carpeta 'algoritmo'
PROYECTO_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(PROYECTO_DIR))
sys.path.append(str(PROYECTO_DIR / "algoritmo"))

# 2. Importamos la Población desde el paquete algoritmo
from algoritmo.poblacion import Poblacion

# ----------------------------------------------------------------------
# CONFIGURACIÓN DEL ENTORNO
# ----------------------------------------------------------------------
WIDTH, HEIGHT = 800, 600
LIFESPAN = 300          # Frames que dura cada generación
POP_SIZE = 50           # Cantidad de cohetes

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Rockets - Algoritmo Genético")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 15)
big_font = pygame.font.SysFont("Consolas", 22, bold=True)

# Geometría y Objetivos
TARGET_POS = pygame.math.Vector2(WIDTH // 2, 60)
TARGET_RADIUS = 20
START_POS = pygame.math.Vector2(WIDTH // 2, HEIGHT - 50)

# Distancia máxima posible en la ventana (diagonal de la pantalla)
# Necesaria para normalizar la función de fitness de tu compañero
MAX_DISTANCIA = math.hypot(WIDTH, HEIGHT)

# Obstáculos en pantalla (Rectángulos de colisión)
OBSTACLES = [
    pygame.Rect(WIDTH // 4 + 50, HEIGHT // 2 - 10, WIDTH // 2 - 100, 20),      # Barrera central
    pygame.Rect(WIDTH // 6, HEIGHT // 4, 120, 15),                              # Lateral izquierdo
    pygame.Rect(WIDTH - WIDTH // 6 - 120, HEIGHT // 4, 120, 15)                 # Lateral derecho
]

# Inicializamos la población real con el código de tu compañero
poblacion = Poblacion(tamano=POP_SIZE, lifespan=LIFESPAN, posicion_inicial=START_POS)

# Variables de control
frame_count = 0
fps_target = 60
paused = False
running = True

# --- Criterio de corte por convergencia (Paciencia) ---
PACIENCIA = 15                  # Máximo de generaciones sin superar el récord de fitness
generaciones_sin_mejora = 0
ultimo_record = 0.0
convergencia_alcanzada = False

# Récord histórico de cohetes que llegaron a la meta
record_cohetes = 0

# ----------------------------------------------------------------------
# FUNCIÓN DE RENDERIZADO DEL COHETE
# (Adapta la posición y velocidad de tu compañero al triángulo de Pygame)
# ----------------------------------------------------------------------
def dibujar_cohete(surface, cohete):
    size = 12
    if cohete.velocidad.length_squared() > 0:
        angle = math.atan2(cohete.velocidad.y, cohete.velocidad.x)
    else:
        angle = -math.pi / 2

    # Vértices del triángulo rotados hacia la dirección de avance
    tip = pygame.math.Vector2(size, 0).rotate_rad(angle) + cohete.posicion
    left = pygame.math.Vector2(-size * 0.6, -size * 0.5).rotate_rad(angle) + cohete.posicion
    right = pygame.math.Vector2(-size * 0.6, size * 0.5).rotate_rad(angle) + cohete.posicion

    # Color según el estado calculado por tu compañero
    if cohete.completado:
        color = (50, 255, 50)    # Verde si llegó a la meta
    elif cohete.chocado:
        color = (180, 50, 50)    # Rojo si chocó con pared u obstáculo
    else:
        color = (220, 220, 255)  # Blanco azulado en vuelo

    pygame.draw.polygon(surface, color, [tip, left, right])

# ----------------------------------------------------------------------
# BUCLE PRINCIPAL DE LA SIMULACIÓN
# ----------------------------------------------------------------------
while running:
    # 1. Eventos y Teclado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_UP:
                fps_target = min(fps_target + 60, 480)   # Acelerar paso de generaciones
            elif event.key == pygame.K_DOWN:
                fps_target = max(fps_target - 60, 60)    # Velocidad normal (60 FPS)
            elif event.key == pygame.K_r:
                poblacion = Poblacion(tamano=POP_SIZE, lifespan=LIFESPAN, posicion_inicial=START_POS)
                frame_count = 0
                generaciones_sin_mejora = 0
                ultimo_record = 0.0
                convergencia_alcanzada = False
                record_cohetes = 0

    # 2. Física y Ciclo Genético (si no está pausado)
    if not paused:
        todos_parados = True
        for c in poblacion.cohetes:
            c.actualizar(frame_count, TARGET_POS, TARGET_RADIUS, OBSTACLES)
            if not c.chocado and not c.completado:
                todos_parados = False

        frame_count += 1

        # Fin de la generación
        if frame_count >= LIFESPAN or todos_parados:
            # 1. Evaluar cohetes
            poblacion.evaluar_poblacion(TARGET_POS, MAX_DISTANCIA)

            # 2. Comprobar si superó el récord anterior (con margen mínimo)
            if poblacion.mejor_fitness_historico > ultimo_record + 0.0005:
                ultimo_record = poblacion.mejor_fitness_historico
                generaciones_sin_mejora = 0  # Resetea el contador si hubo mejora
            else:
                generaciones_sin_mejora += 1 # Suma una generación estancada

            # 3. Evaluar condición de corte
            if generaciones_sin_mejora >= PACIENCIA:
                convergencia_alcanzada = True
                paused = True  # Pausa la simulación automáticamente

            # 4. Solo evoluciona si aún no se alcanzó el corte
            if not convergencia_alcanzada:
                poblacion.evolucionar(k_torneo=2, tasa_mutacion=0.01, elitismo=True)
                frame_count = 0

    # 3. Renderizado del Mundo
    screen.fill((20, 24, 35))

    # Meta
    pygame.draw.circle(screen, (50, 220, 90), (int(TARGET_POS.x), int(TARGET_POS.y)), TARGET_RADIUS)
    pygame.draw.circle(screen, (200, 255, 200), (int(TARGET_POS.x), int(TARGET_POS.y)), TARGET_RADIUS, 3)

    # Obstáculos
    for obs in OBSTACLES:
        pygame.draw.rect(screen, (160, 40, 60), obs, border_radius=4)
        pygame.draw.rect(screen, (220, 80, 100), obs, width=2, border_radius=4)

    # Cohetes
    for c in poblacion.cohetes:
        dibujar_cohete(screen, c)

    # 4. Renderizado del HUD (Métricas en vivo)
    completados = sum(1 for c in poblacion.cohetes if c.completado)
    chocados = sum(1 for c in poblacion.cohetes if c.chocado)

    # Actualiza el récord histórico de cohetes que llegaron a la meta
    if completados > record_cohetes:
        record_cohetes = completados

    ui_lines = [
        f"Generación: {poblacion.generacion}",
        f"Frame: {frame_count}/{LIFESPAN}",
        f"Llegaron a meta: {completados}/{POP_SIZE}",
        f"Récord: {record_cohetes}/{POP_SIZE}",
        f"Estrellados: {chocados}/{POP_SIZE}",
        f"Mejor Fitness: {poblacion.mejor_fitness_historico:.4f}",
        f"Sin mejora: {generaciones_sin_mejora}/{PACIENCIA}",
        f"Velocidad: {fps_target} FPS (UP/DOWN)",
        "Espacio: Pausa | R: Reiniciar"
    ]

    # Panel lateral de fondo
    panel_rect = pygame.Rect(10, 10, 310, len(ui_lines) * 22 + 10)
    pygame.draw.rect(screen, (10, 12, 18, 200), panel_rect, border_radius=6)
    pygame.draw.rect(screen, (60, 70, 90), panel_rect, width=1, border_radius=6)

    for i, line in enumerate(ui_lines):
        txt_surf = font.render(line, True, (230, 230, 240))
        screen.blit(txt_surf, (20, 16 + i * 22))

    # Avisos visuales en pantalla grande
    if convergencia_alcanzada:
        aviso = big_font.render("[CONVERGENCIA ALCANZADA: ÓPTIMO ENCONTRADO]", True, (80, 255, 120))
        screen.blit(aviso, (WIDTH // 2 - aviso.get_width() // 2, HEIGHT - 40))
    elif paused:
        pause_surf = big_font.render("[SIMULACIÓN PAUSADA]", True, (255, 200, 50))
        screen.blit(pause_surf, (WIDTH // 2 - pause_surf.get_width() // 2, HEIGHT - 30))

    pygame.display.flip()
    clock.tick(fps_target)

pygame.quit()