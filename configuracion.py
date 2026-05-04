"""
Parámetros inmutables del escenario y de la ejecución.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ConfiguracionEscenario:
    """
    Todos los datos que definen un escenario de simulación.
    Tiempos en minutos. Tasa de llegada en pasajeros / hora.
    """
    nombre: str
    # Perfil de llegada: Lista de (minuto_inicio, tasa_pasajeros_hora)
    # Ejemplo: [(0, 20), (120, 60), (240, 20)]
    perfil_llegada: list[tuple[float, float]] 
    num_escaneres: int
    num_agentes_revision: int
    num_mostradores_chequeo: int = 3
    chequeo_a: float = 3.0               # Triangular min
    chequeo_m: float = 5.0               # Triangular moda
    chequeo_b: float = 8.0               # Triangular max
    media_escaneo: float = 1.5           # Exponencial
    media_revision: float = 4.0          # Exponencial
    prob_revision: float = 0.15          # Bernoulli
    espera_sala_min: float = 5.0         # Uniforme
    espera_sala_max: float = 20.0        # Uniforme
    media_embarque: float = 3.0          # Exponencial
    tiempo_limite: float = 90.0          # T máximo de ESPERA acumulada
    tiempo_avion_listo: float = 60.0     # Minuto en que el avión está disponible
    duracion_simulacion: float = 480.0   # minutos
    semilla_base: int = 42


@dataclass(frozen=True)
class ParametrosEjecucion:
    """Controla las réplicas y el nivel de confianza."""
    num_replicaciones: int = 30
    nivel_confianza: float = 0.95
