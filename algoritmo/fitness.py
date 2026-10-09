def calcular_fitness_cohete(cohete, meta_pos, max_distancia):
    # Evaluamos por lo más cerca que logró estar de la meta
    distancia = cohete.distancia_minima
    
    fitness = (max_distancia - distancia) / max_distancia
    if fitness < 0:
        fitness = 0

    fitness = fitness ** 2

    if cohete.completado:
        bonus_tiempo = (cohete.lifespan - cohete.tiempo_llegada) / cohete.lifespan
        fitness += 3.0 + bonus_tiempo
    elif cohete.chocado:
        fitness *= 0.5

    return fitness