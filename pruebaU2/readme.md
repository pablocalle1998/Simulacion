# Prueba unidad 2 – Simulación de un Centro de Revision Vehicular
**Autor:** Pablo Calle  
**Materia:** Simulación  

---
# Resultados

## 1. Determinar la cantidad de vehículos atendidos según su tipo.

Lo que se pudo ver en varias ejecuciones de la simulacion, es que la cantidad de vehiculos atentidos varia en funcion de la proporcion con la que el tipo de vehiculo es atendido, es decir, dado que la proporcion de "autos" atendidos es mayor que la de "camiones", los resultados obtenidos con la simulacion nos muesta esta misma tendencia en sus diferentes interaciones. Dandonos un resultado de este estilo:

```bash
Tipo                    	Cantidad

Autos atendidos	              17
Camiones atendidos	          8
```

Lo cual corresponde a lo estipulado en las instrucciones de la simulacion de una relacion del 80% para autos y del 20% para camiones.


---

## 2. Indicar cuantos vehículos están en cada fase según su tipo de vehículo. 

Para este criterio se analiza la cantidad de vehiculos y el tipo de vehiculos que abandonan en cada uno de los puntos del proceso, por exceso de espera.En la simulacion se observo que debido a la fluides y la cantidad de vehiculos que llegan al centro de revision, no es muy comun el abandono del proceso, se obtuvo el siguiente resultado.

```bash
Abandonos antes del escaneo: {'auto': 0, 'camion': 0}
Abandonos antes de revisión: {'auto': 9, 'camion': 0}
```
Habria que considerar que para este criterio se establecio que los camiones nunca abandonan el proceso una vez pasado el proceso de escaneo del vehiculo, a diferencia de los autos los cuales al llegar mas, suelen abandonar en cualquier punto del proceso.

---

## 3. Conclusión o análisis de los datos obtenidos.

### Concluciones

En base a la ejecucion de la simulacion con diferentes parametros puedo asumir que, bajo estos parametros propuestos pareciera que el centro de revision fuera diseñado para atender a una mayor cantidad de vehiculos, ya que el sistema fue diseñado para soportar un volumen mucho más alto del que efectivamente recibe.

Observando los datos de la simulacion vemos que no existe falta de recursos para la atencion del centro, ademas de que la distribucion de los carriles es la adecuada ya que no se producen cuellos de botella. En cuanto al tema de abandonos de algunos vehiculos, realmente el sistema responde de manera adecuada ya que la cantidad de vehiculos que abandonan a la mitad del proceso es bajo como para generar una preocupacion real, es mas, podria decir que el centro de revision estaria en capacidad de soportar incrementos moderados de demanda de servisio en epocas especificas, como lo son los ultimos dias del año.


---
