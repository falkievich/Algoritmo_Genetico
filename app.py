import random
import matplotlib.pyplot as plt  # Importamos matplotlib para los gráficos

# Parámetros del problema
pesos = [
    10, 20, 30, 40, 50, 
    60, 70, 80, 90, 100, 
    15, 25, 35, 45, 55, 
    65, 75, 85, 95, 100
]  # Peso de los objetos

valores = [
    60, 100, 120, 150, 200, 
    250, 300, 350, 400, 450, 
    80, 110, 140, 170, 200, 
    230, 260, 290, 320, 350
]  # Valores de los objetos

capacidad_mochila = 350  # Capacidad máxima de la mochila
tamaño_población = 20  # Número de individuos en la población
tasa_cruce = 0.8  # Probabilidad de cruzar dos individuos
tasa_mutación = 0.1  # Probabilidad de mutación
n_generaciones = 20  # Número de generaciones

# Función para crear un individuo (solución binaria)
def crear_individuo():
    return [random.randint(0, 1) for _ in range(len(pesos))]

# Función de evaluación (fitness)
def calcular_fitness(individuo):
    peso_total = sum(p * i for p, i in zip(pesos, individuo))
    valor_total = sum(v * i for v, i in zip(valores, individuo))  # fitness
    
    if peso_total > capacidad_mochila:  # Penaliza si excede el peso
        return 0  # Mala solución si supera el peso
    else:
        return valor_total  # Retorna el valor total como fitness

# Función de selección por torneo
def seleccion_por_torneo(población, k=3):
    mejor = random.choice(población)
    for _ in range(k - 1):
        individuo = random.choice(población)
        if calcular_fitness(individuo) > calcular_fitness(mejor):  # Se comparan los valores
            mejor = individuo
    return mejor

# Función de cruce (crossover) entre dos individuos
def cruce(individuo1, individuo2):
    if random.random() < tasa_cruce:
        punto_cruce = random.randint(1, len(individuo1) - 1)
        return individuo1[:punto_cruce] + individuo2[punto_cruce:], individuo2[:punto_cruce] + individuo1[punto_cruce:]
    return individuo1, individuo2

# Función de mutación (cambia un bit al azar)
def mutación(individuo):
    for i in range(len(individuo)):
        if random.random() < tasa_mutación:
            individuo[i] = 1 - individuo[i]  # Cambia de 0 a 1 o de 1 a 0
    return individuo

# Función principal del algoritmo genético
def algoritmo_genetico():
    # Crear una población inicial
    población = [crear_individuo() for _ in range(tamaño_población)]
    
    # Listas para almacenar los mejores valores y pesos en cada generación
    mejores_valores = []
    mejores_pesos = []

    # Evolucionar la población
    for generación in range(n_generaciones):
        nueva_población = []
        for _ in range(tamaño_población // 2):
            # Seleccionar dos individuos (padres)
            padre1 = seleccion_por_torneo(población)
            padre2 = seleccion_por_torneo(población)
            
            # Realizar cruce
            hijo1, hijo2 = cruce(padre1, padre2)
            
            # Aplicar mutación
            hijo1 = mutación(hijo1)
            hijo2 = mutación(hijo2)
            
            # Agregar los hijos a la nueva población
            nueva_población.extend([hijo1, hijo2])

        # Reemplazar la población con la nueva generación
        población = nueva_población

        # Encontrar el mejor individuo de la generación actual
        mejor_individuo = max(población, key=calcular_fitness)
        mejor_valor = calcular_fitness(mejor_individuo)
        mejor_peso = sum(p * i for p, i in zip(pesos, mejor_individuo))
        
        # Guardar el mejor valor y peso en las listas
        mejores_valores.append(mejor_valor)
        mejores_pesos.append(mejor_peso)

        print(f"Generación {generación + 1}: Mejor valor = {mejor_valor}, Mochila = {mejor_individuo}")
        print(f"Peso total: {mejor_peso}, Valor total: {mejor_valor}")

    # Devolver el mejor individuo final y los valores/pesos por generación
    mejor_individuo = max(población, key=calcular_fitness)
    return mejor_individuo, mejores_valores, mejores_pesos

# Ejecutar el algoritmo genético y graficar los resultados
mejor_solución, mejores_valores, mejores_pesos = algoritmo_genetico()

# Graficar la evolución del valor (fitness) y el peso a lo largo de las generaciones
generaciones = range(1, n_generaciones + 1)

fig, ax1 = plt.subplots()

# Gráfico de los mejores valores (fitness)
ax1.set_xlabel('Generaciones')
ax1.set_ylabel('Mejor Valor (Fitness)', color='tab:blue')
ax1.plot(generaciones, mejores_valores, color='tab:blue', label='Mejor Valor (Fitness)')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Segundo eje Y para el peso
ax2 = ax1.twinx()
ax2.set_ylabel('Peso Total', color='tab:red')
ax2.plot(generaciones, mejores_pesos, color='tab:red', label='Peso Total')
ax2.axhline(y=capacidad_mochila, color='black', linestyle='--', label='Capacidad Máxima')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Título y leyendas
fig.suptitle('Evolución del Mejor Valor y Peso en el Algoritmo Genético')
fig.tight_layout()
plt.grid(True)

plt.show()

# Imprimir la mejor solución final
print(f"\nMejor solución encontrada: {mejor_solución}")
print(f"Peso total: {sum(p * i for p, i in zip(pesos, mejor_solución))}")
print(f"Valor total: {sum(v * i for v, i in zip(valores, mejor_solución))}")
