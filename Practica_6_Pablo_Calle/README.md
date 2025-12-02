# Práctica 6 – Simulación de un Centro de Urgencias con SimPy
**Autor:** Pablo Calle  
**Materia:** Simulación  


---

Se asume  que es un analista de operaciones en un centro de urgencias de un hospital. Su objetivo es analizar y optimizar 
el flujo de pacientes en el centro de urgencias para garantizar una atención eficiente. El centro de urgencias atiende 
a pacientes con una variedad de problemas médicos, algunos de los cuales requieren más tiempo de atención que 
otros. 

##  Objetivo
El objetivo es minimizar el tiempo de espera promedio de los pacientes en el centro de urgencias. Para lograrlo, 
debes ajustar el número de médicos disponibles en el centro.

---

##  Instrucciones de Simulacion:

• Utiliza SimPy para modelar el flujo de pacientes en el centro de urgencias durante un período de 8 horas. La 
llegada de pacientes sigue una distribución exponencial con una tasa de llegada media de 5 pacientes por 
hora. 
 
• El tiempo de atención de cada paciente sigue una distribución normal, con un tiempo promedio de 20 minutos 
y una desviación estándar de 5 minutos. 
 
• Comienza la simulación con un solo médico disponible en el centro de urgencias. 

---

## 1. Ejecuta la simulación y registra el tiempo promedio de espera de los pacientes en el centro de urgencias después de 8 horas.

Para esta parte de la practica es necesario contar con klos recursos necesarios instalados en el entorno de python, en este caso usaremos Simpy, lo instalamos en nuestro entorno:


```python
pip install simpy
```
Dentro del entorno creado para la simulacion se comienza a ejecutar la simulacion iniciando con el proceso de llegada de los pacientes y definiendo durante cuanto tiempo se ejecutara la simulacion (en minutos), en este caso son 8 horas.

```python
def ejecutar_simulacion(num_medicos):
    env = simpy.Environment()

    hospital = CentroUrgencias(env, num_medicos)

    # Iniciar proceso de llegada de pacientes
    env.process(hospital.llegada_pacientes())

    # Ejecutar simulación durante 8 horas = 480 minutos
    env.run(until=480)

    # Calcular tiempo promedio de espera
    if len(hospital.tiempos_espera) > 0:
        return statistics.mean(hospital.tiempos_espera)
    else:
        return 0
```

Se realiza la simulacion para el primer escenario el cual nos requiere que se simule con solo 1 medico:

```python
espera_1 = ejecutar_simulacion(1)
print(f"Tiempo promedio de espera con 1 médico: {espera_1:.2f} minutos")
```

Esto nos muestra un resultado de 38.17 minutos en esta simulacion en particular:

```bash
Tiempo promedio de espera con 1 médico: 38.17 minutos
```
---

## 2. Luego, repite la simulación con 2 médicos disponibles y registra el nuevo tiempo promedio de espera. 

Ahora se nos pide ejecutar la simualacion en el escenario de contar con 2 medicos en el caso de urgencias.
```python
espera_2 = ejecutar_simulacion(2)
print(f"Tiempo promedio de espera con 2 médicos: {espera_2:.2f} minutos")
```

Esto nos muestra un resultado de 4.78 minutos en esta simulacion en particular:

```bash
Tiempo promedio de espera con 2 médicos: 4.78 minutos
```
---

## 3. Compara los resultados y responde: ¿Cuántos médicos deberían estar disponibles en el centro de urgencias para minimizar el tiempo de espera promedio de los pacientes? 

### Concluciones



- Con **1 médico**, los pacientes acumulan mayor tiempo de espera, esto puede deberse a que la "tasa" de servicio no alcanza a cubrir la demanda de pacientes promedio.

- Con **2 médicos**, el sistema es capaz de atender pacientes de forma más fluida y los tiempos de espera disminuyen de forma notable, aunque al tratarse de un departamento de urgencias siempre se podria mejorar.

Esta claro que se debe considerar el agregar al menos dos medicos en periodos de mayor demanda para que asi se mantenga una estabilidad en la atencion, ademas, se puede considerar el implementar un sistema que ayude a identificar rápidamente los casos mas "simples", los cuales reducen el tiempo de servicio.

Pienso ademas que tambien es necesario distribuir la carga de trabajo entre medicos de manera balanceada y asi evitar "cuellos de botella".


---