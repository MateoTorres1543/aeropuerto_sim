"""
Entidad Pasajero con sus marcas de tiempo.
"""

from typing import Optional


class Pasajero:
    """Guarda los instantes de inicio y fin de cada etapa y gestiona el tiempo T."""

    def __init__(self, id_pasajero: int, t_llegada: float) -> None:
        self.id = id_pasajero
        self.t_llegada = t_llegada
        self.espera_acumulada: float = 0.0
        
        # Para cancelar el evento de "pérdida de vuelo" si entra a servicio a tiempo
        self.evento_perdida_vuelo = None

        self.t_inicio_chequeo: Optional[float] = None
        self.t_fin_chequeo: Optional[float] = None
        # ... (resto de marcas de tiempo iguales)
        self.t_inicio_escaneo: Optional[float] = None
        self.t_fin_escaneo: Optional[float] = None
        self.es_revisado: bool = False
        self.t_inicio_revision: Optional[float] = None
        self.t_fin_revision: Optional[float] = None
        self.t_inicio_sala: Optional[float] = None
        self.t_fin_sala: Optional[float] = None
        self.t_inicio_embarque: Optional[float] = None
        self.t_fin_embarque: Optional[float] = None
        self.pierde_vuelo: bool = False

    @property
    def espera_en_seguridad(self) -> float:
        """
        Tiempo total dentro del proceso de seguridad:
        desde que inicia chequeo hasta que termina escaneo (o revisión).
        Incluye colas dentro de seguridad.
        """
        if self.t_inicio_chequeo is None:
            return 0.0
        fin_seguridad = self.t_fin_revision if self.es_revisado else self.t_fin_escaneo
        if fin_seguridad is None:
            return 0.0
        return max(0.0, fin_seguridad - self.t_inicio_chequeo)

    @property
    def tiempo_en_sistema(self) -> float:
        """Desde llegada hasta que termina embarque o pierde el vuelo."""
        fin = self.t_fin_embarque or self.t_fin_sala or self.t_llegada
        return max(0.0, fin - self.t_llegada)
