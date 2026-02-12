"""
Simulación de Centro de Atención Médica - Red de Colas con SimPy
Evaluación U2 - Red de Colas con simpy.Store
Semilla obligatoria: 77
"""

import simpy
import random


class Paciente:
    """Clase que representa un paciente del centro médico.
    Incluye: ID, tiempo de llegada, tiempos inicio/fin por estación,
    clasificación de prioridad (asignada en Triaje), y si pasó por Farmacia.
    """

    def __init__(self, id_paciente, tiempo_llegada):
        self.id = id_paciente
        self.tiempo_llegada = tiempo_llegada
        self.tiempos_inicio_servicio = {}
        self.tiempos_fin_servicio = {}
        self.prioridad = None  # Se asigna en Triaje: 'ALTA', 'MEDIA', 'BAJA'
        self.fue_a_farmacia = False  # True si pasó por estación 4

    def tiempo_espera_estacion(self, estacion):
        """Calcula el tiempo que el paciente esperó en una estación específica."""
        if estacion in self.tiempos_inicio_servicio:
            if estacion == 0:
                return self.tiempos_inicio_servicio[estacion] - self.tiempo_llegada
            else:
                return (
                    self.tiempos_inicio_servicio[estacion]
                    - self.tiempos_fin_servicio[estacion - 1]
                )
        return None

    def tiempo_total_sistema(self):
        """Tiempo total en el sistema (desde llegada hasta salida).
        Considera si salió tras Consulta o tras Farmacia.
        """
        if self.tiempos_fin_servicio:
            ultima_estacion = max(self.tiempos_fin_servicio.keys())
            return self.tiempos_fin_servicio[ultima_estacion] - self.tiempo_llegada
        return None


class CentroMedico:
    """Simulación de centro de atención médica con red de colas usando simpy.Store.
    Cuatro estaciones secuenciales; ruteo probabilístico 70% a Farmacia tras Consulta.
    """

    def __init__(self, env, config):
        self.env = env
        self.num_estaciones = len(config)
        self.config = config

        # Una Store (cola FIFO) por cada estación
        self.colas = [simpy.Store(env) for _ in range(self.num_estaciones)]

        # Estadísticas por estación
        self.stats = {
            i: {
                'tiempos_espera': [],
                'tiempos_servicio': [],
                'clientes_atendidos': 0,
                'longitud_cola': [],
            }
            for i in range(self.num_estaciones)
        }

        # Pacientes que completaron (con o sin Farmacia)
        self.pacientes_completados = []
        self.pacientes_en_proceso = 0
        self.total_ingresados = 0

        # Iniciar servidores de cada estación
        for estacion_id, cfg in enumerate(config):
            for servidor_id in range(cfg['servidores']):
                env.process(
                    self.servidor(estacion_id, servidor_id + 1, cfg['nombre'])
                )

        # Monitoreo periódico de longitud de colas
        env.process(self.monitorear_colas())

    def _asignar_prioridad(self, paciente):
        """Asigna prioridad en Triaje: 15% Alta, 45% Media, 40% Baja."""
        r = random.random()
        if r < 0.15:
            paciente.prioridad = 'ALTA'
        elif r < 0.60:
            paciente.prioridad = 'MEDIA'
        else:
            paciente.prioridad = 'BAJA'

    def servidor(self, estacion_id, servidor_id, nombre_estacion):
        """Proceso que representa un servidor en una estación."""
        while True:
            paciente = yield self.colas[estacion_id].get()

            paciente.tiempos_inicio_servicio[estacion_id] = self.env.now
            tiempo_espera = paciente.tiempo_espera_estacion(estacion_id)

            # En Triaje (estación 1) asignamos prioridad al iniciar
            if estacion_id == 1:
                self._asignar_prioridad(paciente)
                print(
                    f"{nombre_estacion}-{servidor_id} atiende a Paciente {paciente.id} "
                    f"en tiempo {self.env.now:.2f} (esperó {tiempo_espera:.2f} min)"
                )
                print(f"  -> Paciente {paciente.id} clasificado como: PRIORIDAD {paciente.prioridad}")
            else:
                print(
                    f"{nombre_estacion}-{servidor_id} atiende a Paciente {paciente.id} "
                    f"en tiempo {self.env.now:.2f} (esperó {tiempo_espera:.2f} min)"
                )

            tiempo_servicio = random.uniform(
                self.config[estacion_id]['tiempo_min'],
                self.config[estacion_id]['tiempo_max'],
            )
            yield self.env.timeout(tiempo_servicio)

            paciente.tiempos_fin_servicio[estacion_id] = self.env.now

            self.stats[estacion_id]['tiempos_espera'].append(tiempo_espera)
            self.stats[estacion_id]['tiempos_servicio'].append(tiempo_servicio)
            self.stats[estacion_id]['clientes_atendidos'] += 1

            print(
                f"{nombre_estacion}-{servidor_id} termina con Paciente {paciente.id} "
                f"en tiempo {self.env.now:.2f}"
            )

            # Ruteo según estación
            if estacion_id == 0:
                # Admisión → Triaje
                print(f"  -> Paciente {paciente.id} va a {self.config[1]['nombre']}")
                yield self.colas[1].put(paciente)
            elif estacion_id == 1:
                # Triaje → Consulta Médica
                print(f"  -> Paciente {paciente.id} va a {self.config[2]['nombre']}")
                yield self.colas[2].put(paciente)
            elif estacion_id == 2:
                # Consulta: 70% a Farmacia, 30% sale
                if random.random() < 0.70:
                    print(f"  -> Paciente {paciente.id} va a {self.config[3]['nombre']}")
                    yield self.colas[3].put(paciente)
                else:
                    paciente.fue_a_farmacia = False
                    self.pacientes_completados.append(paciente)
                    self.pacientes_en_proceso -= 1
                    print(f"  [OK] Paciente {paciente.id} sale del centro (sin Farmacia)")
            else:
                # Farmacia (estación 3): sale del sistema
                paciente.fue_a_farmacia = True
                self.pacientes_completados.append(paciente)
                self.pacientes_en_proceso -= 1
                print(f"  [OK] Paciente {paciente.id} sale del centro")

    def monitorear_colas(self):
        """Monitorea la longitud de las colas cada 5 minutos."""
        while True:
            yield self.env.timeout(5)
            for i in range(self.num_estaciones):
                longitud = len(self.colas[i].items)
                self.stats[i]['longitud_cola'].append(longitud)

    def proceso_llegada_pacientes(self):
        """Genera llegadas con distribución exponencial (media 4 min)."""
        paciente_id = 1
        while True:
            paciente = Paciente(paciente_id, self.env.now)
            self.total_ingresados += 1
            self.pacientes_en_proceso += 1
            print(
                f"\n[LLEGADA] Paciente {paciente.id} llega al centro en tiempo {self.env.now:.2f}"
            )
            yield self.colas[0].put(paciente)
            paciente_id += 1
            tiempo_entre_llegadas = random.expovariate(1 / 4)
            yield self.env.timeout(tiempo_entre_llegadas)

    def generar_reporte(self):
        """Genera el reporte con todas las métricas por estación, globales y por prioridad."""
        print("\n" + "=" * 70)
        print("REPORTE DE RED DE COLAS - CENTRO DE ATENCIÓN MÉDICA")
        print("=" * 70)
        print(f"Tiempo de simulación: {self.env.now:.2f} minutos")
        print(f"Número de estaciones: {self.num_estaciones}")
        print(f"Total ingresados: {self.total_ingresados}")
        print(f"Clientes que completaron todo el proceso: {len(self.pacientes_completados)}")
        print(f"Clientes aún en proceso: {self.pacientes_en_proceso}")
        print()

        # A. Métricas por estación (4 estaciones)
        for estacion_id, cfg in enumerate(self.config):
            stats = self.stats[estacion_id]
            print("=" * 70)
            print(f"ESTACIÓN {estacion_id + 1}: {cfg['nombre']}")
            print("=" * 70)
            print("Configuración:")
            print(f"  • Número de servidores: {cfg['servidores']}")
            print(f"  • Tiempo de servicio: {cfg['tiempo_min']:.1f} - {cfg['tiempo_max']:.1f} min")
            print()

            if stats['tiempos_espera']:
                print(f"Clientes atendidos: {stats['clientes_atendidos']}")
                print()
                print("Tiempos de Espera:")
                print(f"  • Promedio: {sum(stats['tiempos_espera']) / len(stats['tiempos_espera']):.2f} min")
                print(f"  • Máximo: {max(stats['tiempos_espera']):.2f} min")
                print(f"  • Mínimo: {min(stats['tiempos_espera']):.2f} min")
                print()
                print("Tiempos de Servicio:")
                print(f"  • Promedio: {sum(stats['tiempos_servicio']) / len(stats['tiempos_servicio']):.2f} min")
                print()
                tiempo_ocupado = sum(stats['tiempos_servicio'])
                tiempo_total = self.env.now * cfg['servidores']
                utilizacion = (tiempo_ocupado / tiempo_total) * 100
                print(f"Utilización de servidores: {utilizacion:.2f}%")
                if stats['longitud_cola']:
                    long_prom = sum(stats['longitud_cola']) / len(stats['longitud_cola'])
                    print(f"Longitud promedio de cola: {long_prom:.2f} pacientes")
            else:
                print("Clientes atendidos: 0")
            print()

        # B. Métricas globales del sistema
        print("=" * 70)
        print("MÉTRICAS GLOBALES DEL SISTEMA")
        print("=" * 70)
        print(f"Total de pacientes que ingresaron: {self.total_ingresados}")
        print(f"Total de pacientes que completaron: {len(self.pacientes_completados)}")

        a_farmacia = sum(1 for p in self.pacientes_completados if p.fue_a_farmacia)
        sin_farmacia = len(self.pacientes_completados) - a_farmacia
        print("Ruteo a Farmacia:")
        if self.pacientes_completados:
            pct_farm = 100 * a_farmacia / len(self.pacientes_completados)
            pct_sin = 100 * sin_farmacia / len(self.pacientes_completados)
            print(f"  • Fueron a Farmacia: {a_farmacia} pacientes ({pct_farm:.1f}%)")
            print(f"  • Salieron directo: {sin_farmacia} pacientes ({pct_sin:.1f}%)")
        print()

        if self.pacientes_completados:
            tiempos_totales = [p.tiempo_total_sistema() for p in self.pacientes_completados]
            print("Tiempo total en el sistema (entrada -> salida):")
            print(f"  • Promedio: {sum(tiempos_totales) / len(tiempos_totales):.2f} min")
            print(f"  • Máximo: {max(tiempos_totales):.2f} min")
            print(f"  • Mínimo: {min(tiempos_totales):.2f} min")
            print()
            throughput = len(self.pacientes_completados) / self.env.now
            print(f"Throughput del sistema: {throughput:.4f} pacientes/min")
            print(f"                        ({throughput * 60:.2f} pacientes/hora)")
        print()

        # C. Análisis por prioridad
        print("=" * 70)
        print("DISTRIBUCIÓN POR PRIORIDAD")
        print("=" * 70)
        completados_con_prioridad = [p for p in self.pacientes_completados if p.prioridad]
        if completados_con_prioridad:
            for prior in ('ALTA', 'MEDIA', 'BAJA'):
                n = sum(1 for p in completados_con_prioridad if p.prioridad == prior)
                pct = 100 * n / len(completados_con_prioridad)
                print(f"  • Prioridad {prior}: {n} pacientes ({pct:.1f}%)")
            print()
            # Comparación de tiempos promedio por prioridad
            print("Tiempo promedio en el sistema por prioridad:")
            for prior in ('ALTA', 'MEDIA', 'BAJA'):
                subset = [p for p in completados_con_prioridad if p.prioridad == prior]
                if subset:
                    prom = sum(p.tiempo_total_sistema() for p in subset) / len(subset)
                    print(f"  • Prioridad {prior}: {prom:.2f} min")
        print("=" * 70)


def main():
    """Ejecuta la simulación completa del centro médico."""
    random.seed(77)

    env = simpy.Environment()

    config = [
        {
            'nombre': 'ADMISIÓN',
            'servidores': 2,
            'tiempo_min': 3,
            'tiempo_max': 7,
        },
        {
            'nombre': 'TRIAJE',
            'servidores': 3,
            'tiempo_min': 5,
            'tiempo_max': 10,
        },
        {
            'nombre': 'CONSULTA MÉDICA',
            'servidores': 4,
            'tiempo_min': 10,
            'tiempo_max': 25,
        },
        {
            'nombre': 'FARMACIA',
            'servidores': 2,
            'tiempo_min': 4,
            'tiempo_max': 8,
        },
    ]

    print("=" * 70)
    print("SIMULACIÓN DE CENTRO DE ATENCIÓN MÉDICA - RED DE COLAS")
    print("=" * 70)
    print(f"Configuración: {len(config)} estaciones en serie")
    for i, cfg in enumerate(config):
        print(f"  Estación {i + 1}: {cfg['nombre']}")
        print(f"    - Servidores: {cfg['servidores']}")
        print(f"    - Tiempo servicio: {cfg['tiempo_min']}-{cfg['tiempo_max']} min")
    print("  Estación 4 FARMACIA: 70% de pacientes (30% sale tras Consulta)")
    print("\nParámetros de llegada:")
    print("  - Distribución: Exponencial")
    print("  - Media entre llegadas: 4 min")
    print("  - Tiempo de simulación: 480 min")
    print("  - Semilla: 77")
    print("=" * 70)

    centro = CentroMedico(env, config)
    env.process(centro.proceso_llegada_pacientes())
    env.run(until=480)
    centro.generar_reporte()


def probar_escenarios():
    """Análisis de sensibilidad (opcional): compara configuración original,
    +1 servidor en la estación más saturada (Consulta), -1 en la menos utilizada (Farmacia).
    Descomentar la llamada abajo para ejecutar.
    """
    escenarios = [
        {
            'nombre': 'Configuración original',
            'config': [
                {'nombre': 'ADMISIÓN', 'servidores': 2, 'tiempo_min': 3, 'tiempo_max': 7},
                {'nombre': 'TRIAJE', 'servidores': 3, 'tiempo_min': 5, 'tiempo_max': 10},
                {'nombre': 'CONSULTA MÉDICA', 'servidores': 4, 'tiempo_min': 10, 'tiempo_max': 25},
                {'nombre': 'FARMACIA', 'servidores': 2, 'tiempo_min': 4, 'tiempo_max': 8},
            ],
        },
        {
            'nombre': '+1 servidor en Consulta (más saturada)',
            'config': [
                {'nombre': 'ADMISIÓN', 'servidores': 2, 'tiempo_min': 3, 'tiempo_max': 7},
                {'nombre': 'TRIAJE', 'servidores': 3, 'tiempo_min': 5, 'tiempo_max': 10},
                {'nombre': 'CONSULTA MÉDICA', 'servidores': 5, 'tiempo_min': 10, 'tiempo_max': 25},
                {'nombre': 'FARMACIA', 'servidores': 2, 'tiempo_min': 4, 'tiempo_max': 8},
            ],
        },
        {
            'nombre': '-1 servidor en Farmacia (menos utilizada)',
            'config': [
                {'nombre': 'ADMISIÓN', 'servidores': 2, 'tiempo_min': 3, 'tiempo_max': 7},
                {'nombre': 'TRIAJE', 'servidores': 3, 'tiempo_min': 5, 'tiempo_max': 10},
                {'nombre': 'CONSULTA MÉDICA', 'servidores': 4, 'tiempo_min': 10, 'tiempo_max': 25},
                {'nombre': 'FARMACIA', 'servidores': 1, 'tiempo_min': 4, 'tiempo_max': 8},
            ],
        },
    ]
    for i, esc in enumerate(escenarios):
        print(f"\n{'#'*70}")
        print(f"ESCENARIO {i+1}: {esc['nombre']}")
        print('#'*70)
        random.seed(77)
        env = simpy.Environment()
        centro = CentroMedico(env, esc['config'])
        env.process(centro.proceso_llegada_pacientes())
        env.run(until=480)
        centro.generar_reporte()


if __name__ == "__main__":
    main()
    probar_escenarios()  # Descomentar para análisis de sensibilidad
