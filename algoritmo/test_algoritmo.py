import pygame
from .poblacion import Poblacion

pygame.init()

def probar_motor_genetico():
    TAMANO_POBLACION = 100
    LIFESPAN = 400
    GENERACIONES = 40
    
    POSICION_INICIAL = pygame.math.Vector2(400, 500)
    META_POS = pygame.math.Vector2(400, 50)
    META_RADIO = 25
    MAX_DISTANCIA = POSICION_INICIAL.distance_to(META_POS)

    obstaculos = [
        pygame.Rect(200, 250, 400, 20)
    ]

    print("==================================================")
    print("   TEST DEL MOTOR GENÉTICO (SMART ROCKETS 2D)   ")
    print("==================================================")
    print(f"Población: {TAMANO_POBLACION} | Frames/Gen: {LIFESPAN} | Torneo k=2\n")

    poblacion = Poblacion(tamano=TAMANO_POBLACION, lifespan=LIFESPAN, posicion_inicial=POSICION_INICIAL)

    for gen in range(1, GENERACIONES + 1):
        for frame in range(LIFESPAN):
            for cohete in poblacion.cohetes:
                cohete.actualizar(frame, META_POS, META_RADIO, obstaculos)

        poblacion.evaluar_poblacion(META_POS, MAX_DISTANCIA)

        mejor_cohete = max(poblacion.cohetes, key=lambda c: c.fitness)
        distancia_al_mejor = mejor_cohete.distancia_minima  # <--- Muestra la cercanía mínima real
        llegaron = sum(1 for c in poblacion.cohetes if c.completado)
        chocaron = sum(1 for c in poblacion.cohetes if c.chocado)

        print(f"Gen {gen:02d} | "
              f"Mejor Fit: {mejor_cohete.fitness:.4f} | "
              f"Dist. a Meta: {distancia_al_mejor:.1f}px | "
              f"Llegaron: {llegaron:02d} | "
              f"Chocaron: {chocaron:02d}")

        if llegaron > TAMANO_POBLACION * 0.7:
            print(f"\n¡Convergencia alcanzada con éxito en la generación {gen}!")
            break

        dnas_nuevos = poblacion.evolucionar(k_torneo=2, tasa_mutacion=0.01)

    print("\n==================================================")
    print("          TEST FINALIZADO CORRECTAMENTE          ")
    print("==================================================")

if __name__ == "__main__":
    probar_motor_genetico()