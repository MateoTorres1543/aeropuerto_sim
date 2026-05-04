"""
Estructuras de datos para almacenar métricas de simulación.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict


@dataclass
class MetricasEstacion:
    nombre: str
    max_cola: int
    promedio_cola: float
    utilizacion: float


@dataclass
class MetricasReplica:
    total: int
    perdidos: int
    esperas_seguridad: List[float]
    tiempos_sistema: List[float]
    estaciones: Dict[str, MetricasEstacion]

    @property
    def pct_perdidos(self) -> float:
        return (100.0 * self.perdidos / self.total) if self.total else 0.0

    @property
    def media_espera(self) -> float:
        if not self.esperas_seguridad:
            return 0.0
        return sum(self.esperas_seguridad) / len(self.esperas_seguridad)


@dataclass
class ResultadoEscenario:
    nombre: str
    total_pasajeros: float
    media_espera: float
    ic_espera: Tuple[float, float]
    pct_perdidos: float
    ic_perdidos: Tuple[float, float]
    
    # Métricas agregadas de estaciones
    met_estaciones: Dict[str, Dict[str, float]] # nombre -> {max_cola, prom_cola, utilizacion}
    
    replicas: List[MetricasReplica]
    todas_esperas: List[float]
    todos_tiempos_sistema: List[float]
