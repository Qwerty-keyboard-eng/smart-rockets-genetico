import random
import pygame

class DNA:
    def __init__(self, lifespan, genes=None):
        self.lifespan = lifespan
        
        if genes is not None:
            self.genes = genes
        else:
            self.genes = []
            for _ in range(self.lifespan):
                fuerza = pygame.math.Vector2()
                fuerza.from_polar((1, random.uniform(0, 360)))
                fuerza.scale_to_length(random.uniform(0, 0.8))
                self.genes.append(fuerza)

    def cruzar(self, otro_dna):
        """Cruce en un punto: Preserva tramos continuos de movimiento."""
        punto_corte = random.randint(1, self.lifespan - 1)
        nuevos_genes = self.genes[:punto_corte] + otro_dna.genes[punto_corte:]
        return DNA(self.lifespan, genes=nuevos_genes)

    def mutar(self, tasa_mutacion=0.02):
        """Mutación: Reemplaza o altera levemente vectores según probabilidad."""
        for i in range(self.lifespan):
            if random.random() < tasa_mutacion:
                fuerza = pygame.math.Vector2()
                fuerza.from_polar((1, random.uniform(0, 360)))
                fuerza.scale_to_length(random.uniform(0, 0.8))
                self.genes[i] = fuerza