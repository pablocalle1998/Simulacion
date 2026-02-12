# Evaluación Red de Colas - Centro Médico

## Estudiante

- **Nombre**: Pablo Sebastian Calle Ortega
- **Fecha**: 12/febrero/2026

## Descripción del Sistema

En este proyecto se propone implementar un centro de atencion medica, utilizando como modelado una red de colas, esto, haciendo uso de herramientas como Simpy para cada estacion propuesta. En el experimento, los pacientes pasan de forma ordenada por cuatro estaciones: Admisión, Triaje, Consulta Médica y Farmacia . En Triaje se asigna a cada paciente una prioridad (Alta 15%, Media 45%, Baja 40%) que se registra para análisis. Las llegadas siguen una distribución exponencial y los tiempos de servicio son uniformes según la configuración de cada estación.

## Configuración de la Simulación

- **Semilla**: 77
- **Tiempo de simulación**: 480 minutos (8 horas)
- **Llegadas**: Exponencial con media 4 minutos
- **Estaciones**: 4 

    Admisión: 2 servidores 3–7 min

    Triaje: 3 servidores 5–10 min

    Consulta: 4 servidores 10–25 min 

    Farmacia: 2 servidores 4–8 min

## Resultados Obtenidos


### Métricas por Estación

| Estación   | Atendidos | Espera prom (min) | Espera máx (min) | Servicio prom (min) | Utilización | Long. prom cola |
|-----------|-----------|-------------------|------------------|---------------------|-------------|------------------|
| ADMISIÓN  | 141       | 3.74              | 18.90            | 4.89                | 71.81%      | 1.14             |
| TRIAJE    | 138       | 0.95              | 5.86             | 7.53                | 72.14%      | 0.24             |
| CONSULTA  | 103       | 46.07             | 122.52           | 17.25               | 92.55%      | 15.96            |
| FARMACIA  | 75        | 0.27              | 3.58             | 6.01                | 46.93%      | 0.05             |

### Métricas Globales

- **Total ingresados**: 142
- **Total completaron**: 102
- **Fueron a Farmacia**: 75 (73.5%)
- **Salieron directo**: 27 (26.5%)
- **Tiempo total en sistema**: 

        promedio 85.34 min

        máximo 163.59 min

        mínimo 24.38 min
- **Throughput (rendimiento)**: 12.75 pacientes/hora

### Análisis por Prioridad

- Prioridad Alta: 17 (16.7%)
- Prioridad Media: 36 (35.3%)
- Prioridad Baja: 49 (48.0%)

Tiempo promedio en el sistema por prioridad: 

    Alta 86.33 min, 
    Media 85.11 min, 
    Baja 85.16 min. 

Como se ve las diferencias son pequeñas entre cada una de las distintas "prioridades", esto se puede deber a que en elmodelo que se propone no se establecieron "colas prioritarias".

## Análisis de Datos

### Cuellos de Botella Identificados

Tomando en cuenta los resultados que se obtuvierion durante la simulacion se logro resaltar algunos aspecto de las estaciones de trabajo que se proponen durante el ejercicio, por ejemplo:

La estación con **mayor longitud promedio de cola** es CONSULTA MÉDICA, esta estacion cuenta con 15.96 pacientes de media esperando. Si lo comparamos con las demas estaciones (Admisión 1.14, Triaje 0.24, Farmacia 0.05) esto nos puede indicar que los pacientes se acumulan sobre todo antes de ser atendidos por el médico, esto ya en un caso practico en un "escenario real".

Los **mayores tiempos de espera** también se concentran en CONSULTA MÉDICA. Al ver los resultados de la simulacion el promedio es de 46.07 minutos y el máximo alcanza 122.52 minutos. Hay que tomar en cuenta que, en ninguna otra estación se superan los 19 minutos de espera máxima, por lo tanto CONSULTA MÉDICA es claramente el punto donde la demora parece ser más crítica para el paciente.

En cuanto a la **utilización de servidores**, CONSULTA MÉDICA vuelve a sobresalir  con un 92.55%, la más alta de todo el sistema. 

Precisamente por estos resultados Consulta Médica estaria sobresaturada con utilización mayor al 90%, lo que confirma que los cuatro doctores están trabajando casi al límite y que cualquier "pico" de demanda se traduce en colas largas y esperas elevadas.

Por el contrario, la estacion de FARMACIA presenta una utilización del 46.93% por lo cual se la podria considerar subutilizada. Verificando en las demas estaciones Admisión y Triaje se mantienen al rededor del 72%. 

Puedo concluir que el Cuello de Botella se encuentra en el area de CONSULTA MEDICA, siendo uno de los factores determinantes en el estres de esta simulacion, siendo necesaria una implementacion de cambio en esta estacion, ademas la estacion de Farmacia tiene aun mayor disponibilidad lo cual alijera un poco el peso del flujo del sistema.

### Diagnóstico del Sistema

La **estación más problemática** es CONSULTA MÉDICA. En ella confluyen la mayor utilización (92.55%), la cola más larga (15.96 pacientes de promedio) y los tiempos de espera más altos (46 minutos de media, con casos extremos por encima de dos horas). Es ahí donde el sistema se desborda y donde cualquier mejora tendrá el mayor impacto.

Para determinar si los tiempos de espera son aceptables se debe tomar en cuenta la referencia de 15 minutos, la conclusión es que en Admisión y Triaje si, ls tiempos de espera son razonables. En cambio, en Consulta no son aceptables el promedio de 46 minutos y los máximos superiores a 120 minutos se consideran directamente como una experiencia de espera muy negativa.



## Validación: resultados de probar_escenarios

Se intento realizar la propuesta de que pasaría con el cambio en dos escenarios diferentes que son añadir un servidor en Consulta y quitar uno en Farmacia, se ejecutó la función `probar_escenarios()` con la misma semilla 77. A continuación se presenta una tabla comparativa entre el escenario original y los dos escenarios de sensibilidad.

| Métrica | Original | +1 servidor en Consulta | -1 servidor en Farmacia |
|--------|----------|--------------------------|--------------------------|
| **Utilización de estacion: ADMISIÓN** | 71.8% | 66.9% | 63.8% |
| **Utilización de estacion: TRIAJE** | 72.1% | 66.5% | 64.1% |
| **Utilización de estacion: CONSULTA** | 92.5% | 80.3% | 89.6% |
| **Utilización de estacion: FARMACIA** | 46.9% | 47.5% | 76.0% |
| **Espera promedio ADMISIÓN (min)** | 3.74 | 1.76 | 2.08 |
| **Espera promedio TRIAJE (min)** | 0.95 | 0.47 | 0.40 |
| **Espera promedio CONSULTA (min)** | 46.07 | 3.43 | 29.23 |
| **Espera promedio FARMACIA (min)** | 0.27 | 0.48 | 9.96 |
| **Pacientes completados** | 102 | 114 | 100 |
| **Tiempo total promedio (min)** | 85.34 | 39.26 | 69.60 |

**Concluciones de esta prueba de escenarios:** 

Con **+1 servidor en Consulta** la utilización en esa estación baja de 92.5% a 80.3%, la espera promedio en Consulta pasa de 46.07 min a 3.43 min, el tiempo total promedio en el sistema baja a 39.26 min. Esto nos muestra lo necesario que es el aumentar capacidad en Consulta ya que se tendría un impacto muy positivo. 

Con **-1 servidor en Farmacia** la utilización de Farmacia sube al 76%, la espera en Farmacia pasa a 9.96 min y la cola a 1.45 min, sin embargo el tiempo total empeora respecto al original, lo que nos mostraria que no conviene reducir recursos en farmacia con la configuración actual.

## Conclusiones y Recomendaciones

En base del analisis general de la propuesta de simulacion y el análisis de los datos de la simulación se plantearon tres propuestas de mejora concretas.

**Propuesta 1: Aumentar el número de servidores en CONSULTA MÉDICA.** 

La utilización actual del 92.55%, la cola promedio de 15.96 pacientes y el tiempo de espera promedio de 46.07 minutos (con máximos de 122.52 minutos) claramente nos muestran que el area de Consulta es la única estación que esta, por mucho, saturada. En un escenario real, añadir un quinto doctor permitiría reducir la utilización y jutno con esto la longitud de la cola y los tiempos de espera en esta estación. El impacto que se tendria es una mejora directa del tiempo total que los pacientes pasan en el sistema y tambien de la percepción de calidad del servicio, sin necesidad de realizar cambios en el resto de estaciones.

**Propuesta 2: Mantener la capacidad actual en FARMACIA y evaluar la reasignacion de sus recursos.**

 La estacion de FARMACIA presenta una utilización del 46.93% (por debajo del 50%) y una cola promedio de 0.05 pacientes, por lo que no actúa como cuello de botella y tiene margen suficiente para atender el 70% del flujo que sale de Consulta. No se recomienda en este momento con los parametros actuales añadir más estaciones de farmacia. En el caso de que en el futuro se implementa la Propuesta 1 antes comentada y se llegara a aumentar el flujo que llega a Farmacia, sería el momento de revisar de nuevo sus métricas antes de plantear reducciones de personal, para no generar un nuevo cuello de botella.

**Propuesta 3: Reducir , si es posible, el tiempo medio de servicio en CONSULTA.** 

La estacion de Consulta tiene un rango de servicio más amplio (10–25 minutos) y la mayor carga del sistema. Esto nos puede revelar que la congestion que se genera, no solo se debe al número de servidores, sino tambien a la duración de cada consulta. Esta medida se propone tambien como un complemetno de la propuesta 1, esto quiere decir que se puede llegar a combinar un doctor mas, con una mejora de la eficiencia del proceso para obtener un efecto mayor sobre los tiempos de espera y la utilización.

## Instrucciones de Ejecución

Requisitos: Python 3.x y la librería SimPy (`pip install simpy`).

```bash
python PABLO_CALLE_PRUEBAU2_REDCOLAS.py
```


