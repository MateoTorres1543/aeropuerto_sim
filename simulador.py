"""
Ejecutor de múltiples réplicas con cálculo de intervalos de confianza.
"""

import math
import random
from typing import Callable, Optional, List, Tuple, Dict

from configuracion import ConfiguracionEscenario, ParametrosEjecucion
from motor_des import MotorDES
from proceso_aeropuerto import ProcesoAeropuerto
from resultado import MetricasReplica, ResultadoEscenario, MetricasEstacion


def _media(valores: List[float]) -> float:
    return sum(valores) / len(valores) if valores else 0.0

def _desviacion_estandar(valores: List[float]) -> float:
    if len(valores) < 2:
        return 0.0
    m = _media(valores)
    return math.sqrt(sum((x - m) ** 2 for x in valores) / (len(valores) - 1))

def _intervalo_confianza(valores: List[float], nivel: float) -> Tuple[float, float]:
    if not valores:
        return (0.0, 0.0)
    z = {0.90: 1.645, 0.95: 1.960, 0.99: 2.576}.get(nivel, 1.960)
    m = _media(valores)
    margen = z * _desviacion_estandar(valores) / math.sqrt(len(valores))
    return (m - margen, m + margen)


class Simulador:
    def __init__(self, cfg: ConfiguracionEscenario, params: ParametrosEjecucion) -> None:
        self._cfg = cfg
        self._params = params

    def ejecutar(self, callback_progreso: Optional[Callable] = None) -> ResultadoEscenario:
        replicas: List[MetricasReplica] = []
        n = self._params.num_replicaciones

        for i in range(n):
            semilla = self._cfg.semilla_base + i
            rng = random.Random(semilla)
            motor = MotorDES(self._cfg.duracion_simulacion)
            proceso = ProcesoAeropuerto(self._cfg, motor, rng)
            proceso.iniciar()
            motor.ejecutar()
            replicas.append(self._recolectar(proceso))

            if callback_progreso:
                callback_progreso(i + 1, n)

        return self._agregar(replicas)

    def _recolectar(self, proceso: ProcesoAeropuerto) -> MetricasReplica:
        esperas, t_sistema = [], []
        perdidos = total = 0
        for p in proceso.pasajeros:
            if p.t_inicio_chequeo is None:
                continue
            total += 1
            esperas.append(p.espera_en_seguridad)
            t_sistema.append(p.tiempo_en_sistema)
            if p.pierde_vuelo:
                perdidos += 1
        
        # Recolectar datos de TODAS las estaciones
        estaciones = {}
        for est in [proceso.chequeo, proceso.escaneo, proceso.revision, proceso.puerta_a, proceso.puerta_b]:
            estaciones[est.nombre] = MetricasEstacion(
                nombre=est.nombre,
                max_cola=est.max_cola,
                promedio_cola=est.longitud_promedio_cola(),
                utilizacion=est.utilizacion()
            )
            
        return MetricasReplica(total, perdidos, esperas, t_sistema, estaciones)

    def _agregar(self, replicas: List[MetricasReplica]) -> ResultadoEscenario:
        medias_espera   = [r.media_espera for r in replicas]
        pcts_perdidos   = [r.pct_perdidos for r in replicas]
        totales         = [r.total for r in replicas]
        todas_esperas   = [e for r in replicas for e in r.esperas_seguridad]
        todos_sistema   = [t for r in replicas for t in r.tiempos_sistema]

        # Agregar métricas por estación
        nombres_est = list(replicas[0].estaciones.keys())
        met_estaciones = {}
        for nombre in nombres_est:
            met_estaciones[nombre] = {
                "max_cola": _media([r.estaciones[nombre].max_cola for r in replicas]),
                "prom_cola": _media([r.estaciones[nombre].promedio_cola for r in replicas]),
                "utilizacion": _media([r.estaciones[nombre].utilizacion for r in replicas])
            }

        return ResultadoEscenario(
            nombre=self._cfg.nombre,
            total_pasajeros=_media(totales),
            media_espera=_media(medias_espera),
            ic_espera=_intervalo_confianza(medias_espera, self._params.nivel_confianza),
            pct_perdidos=_media(pcts_perdidos),
            ic_perdidos=_intervalo_confianza(pcts_perdidos, self._params.nivel_confianza),
            met_estaciones=met_estaciones,
            replicas=replicas,
            todas_esperas=todas_esperas,
            todos_tiempos_sistema=todos_sistema
        )
