import random
from .cohete import Cohete
from .fitness import calcular_fitness_cohete

class Poblacion:
    def __init__(self, tamano, lifespan, posicion_inicial):
        self.tamano = tamano
        self.lifespan = lifespan
        self.posicion_inicial = posicion_inicial
        
        self.cohetes = [Cohete(lifespan, posicion_inicial) for _ in range(tamano)]
        self.generacion = 1
        self.mejor_fitness_historico = 0.0

    def evaluar_poblacion(self, meta_pos, max_distancia):
        """Calcula el fitness de cada cohete."""
        max_fit = 0.0
        for cohete in self.cohetes:
            cohete.fitness = calcular_fitness_cohete(cohete, meta_pos, max_distancia)
            if cohete.fitness > max_fit:
                max_fit = cohete.fitness
                
        if max_fit > self.mejor_fitness_historico:
            self.mejor_fitness_historico = max_fit

    def seleccion_torneo(self, k=2):
        """SELECCIÓN POR TORNEO DETERMINISTA (k)"""
        aspirantes = random.sample(self.cohetes, k)
        ganador = max(aspirantes, key=lambda c: c.fitness)
        return ganador

    def evolucionar(self, k_torneo=2, tasa_mutacion=0.01, elitismo=True):
        """
        Crea la nueva generación con Elitismo (Top 2) + Torneo + Cruce Uniforme + Mutación.
        """
        nuevos_cohetes = []
        
        # Ordenamos los cohetes de mejor a peor fitness
        cohetes_ordenados = sorted(self.cohetes, key=lambda c: c.fitness, reverse=True)

        # 1. Elitismo: Conservamos los 2 mejores sin alterar
        if elitismo:
            cant_elites = min(2, len(self.cohetes))
            for i in range(cant_elites):
                elite_dna = cohetes_ordenados[i].dna
                nuevos_cohetes.append(Cohete(self.lifespan, self.posicion_inicial, elite_dna))

        # 2. Reproducción por Selección por Torneo
        while len(nuevos_cohetes) < self.tamano:
            padre1 = self.seleccion_torneo(k=k_torneo)
            padre2 = self.seleccion_torneo(k=k_torneo)
            
            # Cruce Uniforme y Mutación
            hijo_dna = padre1.dna.cruzar(padre2.dna)
            hijo_dna.mutar(tasa_mutacion)
            
            nuevos_cohetes.append(Cohete(self.lifespan, self.posicion_inicial, hijo_dna))

        self.cohetes = nuevos_cohetes
        self.generacion += 1