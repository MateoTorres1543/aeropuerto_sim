"""
Estación de servicio genérica con múltiples servidores en paralelo.
Soporta cálculo de longitud promedio de cola mediante integración temporal.
"""

from collections import deque
from typing import Callable, Deque, Optional


class EstacionServicio:
    """Modela una cola FIFO con N servidores idénticos y soporte para bloqueos."""

    def __init__(self, nombre: str, num_servidores: int, motor) -> None:
        self.nombre = nombre
        self._motor = motor
        self._servidores_libres = num_servidores
        self._num_servidores = num_servidores
        self._esta_disponible = True  # Para bloquear embarque
        self._cola: Deque = deque()
        
        # Estadísticas... (mantener igual)
        self._max_cola = 0
        self._area_cola = 0.0
        self._t_ultimo_cambio = 0.0
        self._tiempo_ocupado = 0.0

    @property
    def max_cola(self) -> int:
        return self._max_cola

    def utilizacion(self) -> float:
        """Fracción de tiempo que los servidores estuvieron ocupados [0, 1]."""
        capacidad_total = self._motor.duracion * self._num_servidores
        return min(1.0, self._tiempo_ocupado / capacidad_total) if capacidad_total else 0.0

    def longitud_promedio_cola(self) -> float:
        """Calcula Lq = (1/T) * sum(longitud * duracion)."""
        self._actualizar_area_cola()
        return self._area_cola / self._motor.duracion if self._motor.duracion > 0 else 0.0

    def _actualizar_area_cola(self) -> None:
        t_actual = self._motor.tiempo_actual
        delta_t = t_actual - self._t_ultimo_cambio
        self._area_cola += len(self._cola) * delta_t
        self._t_ultimo_cambio = t_actual

    def set_disponible(self, estado: bool) -> None:
        """Activa o desactiva la atención (e.g. avión listo)."""
        self._esta_disponible = estado
        if estado:
            self._intentar_atender_cola()

    def atender(self,
                pasajero,
                duracion: float,
                callback_terminado: Callable,
                callback_inicio: Optional[Callable] = None,
                callback_fin: Optional[Callable] = None,
                t_limite_espera: Optional[float] = None,
                callback_timeout: Optional[Callable] = None) -> None:
        
        self._actualizar_area_cola()
        t_actual = self._motor.tiempo_actual
        
        # Si hay servidores libres y está disponible, entrar directo
        if self._servidores_libres > 0 and self._esta_disponible:
            self._iniciar_servicio(pasajero, duracion, callback_terminado,
                                   callback_inicio, callback_fin)
        else:
            # Añadir a cola con posible timeout (Requisito T)
            item = [pasajero, duracion, callback_terminado, callback_inicio, callback_fin, t_actual]
            self._cola.append(item)
            self._max_cola = max(self._max_cola, len(self._cola))

            if t_limite_espera is not None and callback_timeout:
                def al_perder_vuelo():
                    if item in self._cola:
                        self._actualizar_area_cola()
                        self._cola.remove(item)
                        # Registrar espera parcial antes de salir
                        pasajero.espera_acumulada += (self._motor.tiempo_actual - item[5])
                        callback_timeout(pasajero)

                pasajero.evento_perdida_vuelo = self._motor.programar(
                    t_actual + t_limite_espera, al_perder_vuelo
                )

    def _intentar_atender_cola(self) -> None:
        while self._cola and self._servidores_libres > 0 and self._esta_disponible:
            self._actualizar_area_cola()
            p, d, cb, ci, cf, t_entrada = self._cola.popleft()
            
            # Registrar espera acumulada real
            p.espera_acumulada += (self._motor.tiempo_actual - t_entrada)
            
            # Cancelar el evento de timeout si existía
            if hasattr(p, 'evento_perdida_vuelo') and p.evento_perdida_vuelo:
                self._motor.cancelar(p.evento_perdida_vuelo)
                p.evento_perdida_vuelo = None

            self._iniciar_servicio(p, d, cb, ci, cf)

    def _iniciar_servicio(self, pasajero, duracion, callback_terminado,
                          callback_inicio, callback_fin) -> None:
        self._servidores_libres -= 1
        t_inicio = self._motor.tiempo_actual

        if callback_inicio:
            callback_inicio(pasajero, t_inicio)

        def al_terminar():
            t_fin = self._motor.tiempo_actual
            self._tiempo_ocupado += (t_fin - t_inicio)

            if callback_fin:
                callback_fin(pasajero, t_fin)

            self._servidores_libres += 1
            self._intentar_atender_cola()
            callback_terminado(pasajero)

        self._motor.programar(t_inicio + duracion, al_terminar)
