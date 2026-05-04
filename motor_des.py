"""
Motor de Simulación de Eventos Discretos.
Utiliza un min‑heap para procesar eventos en orden cronológico.
"""

import heapq
from typing import Callable, List, Tuple

Evento = Tuple[float, int, Callable[[], None]]


class MotorDES:
    """Controla el reloj de simulación y despacha eventos."""

    def __init__(self, duracion: float) -> None:
        self.duracion = duracion
        self.tiempo_actual = 0.0
        self._heap: List[Evento] = []
        self._orden = 0
        self._cancelados: set[int] = set()

    def programar(self, instante: float, accion: Callable[[], None]) -> int:
        """Agenda un evento futuro y devuelve su ID para cancelación."""
        if instante > self.duracion:
            return -1
        id_ev = self._orden
        heapq.heappush(self._heap, (instante, id_ev, accion))
        self._orden += 1
        return id_ev

    def cancelar(self, id_evento: int) -> None:
        """Marca un evento para ser ignorado."""
        if id_evento != -1:
            self._cancelados.add(id_evento)

    def ejecutar(self) -> None:
        """Procesa todos los eventos en orden."""
        while self._heap:
            t, id_ev, accion = heapq.heappop(self._heap)
            if t > self.duracion:
                break
            if id_ev in self._cancelados:
                self._cancelados.remove(id_ev)
                continue
            self.tiempo_actual = t
            accion()

    def reiniciar(self) -> None:
        """Limpia el motor para una nueva réplica."""
        self.tiempo_actual = 0.0
        self._heap.clear()
        self._orden = 0
        self._cancelados.clear()
