import pygame
import math

class Rocket:
    def __init__(self, x, y, dna):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.dna = dna
        
        # Estados
        self.crashed = False
        self.completed = False
        self.finish_time = 0  # Frame exacto en el que tocó la meta

        # Parámetros físicos
        self.max_speed = 6.0
        self.size = 12  # Longitud del cohete en píxeles

    def apply_force(self, force):
        self.acc += force

    def update(self, step, target_pos, target_radius, obstacles, screen_rect):
        """Avanza la física en cada frame si el cohete sigue activo."""
        if self.crashed or self.completed:
            return

        # 1. Aplicar el gen correspondiente al frame actual
        if step < len(self.dna.genes):
            self.apply_force(self.dna.genes[step])

        # 2. Integración física
        self.vel += self.acc
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)
        self.pos += self.vel
        self.acc *= 0  # Reiniciar aceleración

        # 3. Detección de colisión con la Meta
        if self.pos.distance_to(target_pos) <= target_radius:
            self.completed = True
            self.finish_time = step
            self.pos = pygame.math.Vector2(target_pos)  # Anclar al centro

        # 4. Detección de colisión con Bordes de la pantalla
        if not screen_rect.collidepoint(self.pos.x, self.pos.y):
            self.crashed = True

        # 5. Detección de colisión con Obstáculos
        for obs in obstacles:
            if obs.collidepoint(self.pos.x, self.pos.y):
                self.crashed = True
                break

    def draw(self, surface):
        """Dibuja el cohete como un triángulo orientado hacia su dirección de avance."""
        if self.vel.length_squared() > 0:
            angle = math.atan2(self.vel.y, self.vel.x)
        else:
            angle = -math.pi / 2  # Apuntar hacia arriba si está quieto

        # Vértices locales (punta, ala izquierda, ala derecha)
        tip = pygame.math.Vector2(self.size, 0).rotate_rad(angle) + self.pos
        left = pygame.math.Vector2(-self.size * 0.6, -self.size * 0.5).rotate_rad(angle) + self.pos
        right = pygame.math.Vector2(-self.size * 0.6, self.size * 0.5).rotate_rad(angle) + self.pos

        # Color según estado
        if self.completed:
            color = (50, 255, 50)    # Verde si llegó
        elif self.crashed:
            color = (180, 50, 50)    # Rojo apagado si chocó
        else:
            color = (220, 220, 255)  # Blanco azulado en vuelo

        pygame.draw.polygon(surface, color, [tip, left, right])