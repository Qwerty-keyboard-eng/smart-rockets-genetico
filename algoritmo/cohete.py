import pygame
from .dna import DNA

class Cohete:
    def __init__(self, lifespan, posicion_inicial, dna=None):
        if dna is None:
            self.dna = DNA(lifespan)
        else:
            self.dna = dna
            
        self.lifespan = lifespan
        self.posicion = pygame.math.Vector2(posicion_inicial)
        self.velocidad = pygame.math.Vector2(0, 0)
        self.aceleracion = pygame.math.Vector2(0, 0)
    
        
        self.chocado = False
        self.completado = False
        self.tiempo_llegada = 0
        self.fitness = 0.0
        self.distancia_minima = float('inf')
        self.max_speed = 5.0  # <-- AGREGAR ESTA LÍNEA

    def aplicar_fuerza(self, fuerza):
        if not self.chocado and not self.completado:
            self.aceleracion += fuerza

    def actualizar(self, frame, meta_pos, meta_radio, obstaculos):
        if self.chocado or self.completado:
            return

        # 1. Movimiento físico
        self.aplicar_fuerza(self.dna.genes[frame])
        self.velocidad += self.aceleracion

        # Limitar la velocidad máxima para que puedan doblar
        if self.velocidad.length() > self.max_speed:
            self.velocidad.scale_to_length(self.max_speed)

        self.posicion += self.velocidad
        self.aceleracion *= 0

        # 2. Registrar cercanía mínima ANTES de evaluar colisiones
        dist_a_meta = self.posicion.distance_to(meta_pos)
        if dist_a_meta < self.distancia_minima:
            self.distancia_minima = dist_a_meta

        # 3. Evaluar llegada a meta
        if dist_a_meta < meta_radio:
            self.completado = True
            self.tiempo_llegada = frame
            return

        # 4. Evaluar choque con obstáculos
        for obstaculo in obstaculos:
            if obstaculo.collidepoint(self.posicion.x, self.posicion.y):
                self.chocado = True
                return

        # 5. Evaluar colisión con límites de ventana
        if self.posicion.x < 0 or self.posicion.x > 800 or self.posicion.y < 0 or self.posicion.y > 600:
            self.chocado = True
            return