"""
Implementa el flujo completo del aeropuerto.
"""

import random
from configuracion import ConfiguracionEscenario
from distribuciones import Distribuciones
from motor_des import MotorDES
from estacion_servicio import EstacionServicio
from pasajero import Pasajero


class ProcesoAeropuerto:
    """Coordina el paso de cada pasajero por las estaciones cumpliendo requisitos T."""

    def __init__(self, cfg: ConfiguracionEscenario, motor: MotorDES, rng: random.Random) -> None:
        self.cfg = cfg
        self.motor = motor
        self.rng = rng
        self._pasajeros: list[Pasajero] = []
        self._proximo_id = 1

        # Estaciones
        self.chequeo   = EstacionServicio("Chequeo",   cfg.num_mostradores_chequeo, motor)
        self.escaneo   = EstacionServicio("Escáner",   cfg.num_escaneres, motor)
        self.revision  = EstacionServicio("Revisión",  cfg.num_agentes_revision, motor)
        self.puerta_a  = EstacionServicio("Puerta A",  1, motor)
        self.puerta_b  = EstacionServicio("Puerta B",  1, motor)

        # Estado inicial: Puertas bloqueadas hasta que el avión esté listo
        self.puerta_a.set_disponible(False)
        self.puerta_b.set_disponible(False)

    def iniciar(self) -> None:
        """Programa la primera llegada y el evento de avión listo."""
        self._programar_llegada()
        self.motor.programar(self.cfg.tiempo_avion_listo, self._avion_llega)

    def _avion_llega(self) -> None:
        """Libera el proceso de embarque."""
        self.puerta_a.set_disponible(True)
        self.puerta_b.set_disponible(True)

    def _obtener_tasa_actual(self) -> float:
        """Calcula la tasa lambda basada en el perfil de llegada."""
        t_actual = self.motor.tiempo_actual
        tasa = 0.0
        for inicio, val in sorted(self.cfg.perfil_llegada):
            if t_actual >= inicio:
                tasa = val
            else:
                break
        return max(0.0001, tasa)

    def _programar_llegada(self) -> None:
        tasa = self._obtener_tasa_actual()
        media_entre_llegadas = 60.0 / tasa
        intervalo = Distribuciones.exponencial(media_entre_llegadas, self.rng)
        self.motor.programar(self.motor.tiempo_actual + intervalo, self._evento_llegada)

    def _perdida_vuelo_timeout(self, p: Pasajero) -> None:
        """Rutina de interrupción por superar tiempo T de espera."""
        p.pierde_vuelo = True

    def _evento_llegada(self) -> None:
        p = Pasajero(self._proximo_id, self.motor.tiempo_actual)
        self._proximo_id += 1
        self._pasajeros.append(p)

        # Enviar a chequeo con control de tiempo T
        duracion_chequeo = Distribuciones.triangular(
            self.cfg.chequeo_a, self.cfg.chequeo_m, self.cfg.chequeo_b, self.rng
        )
        t_restante = self.cfg.tiempo_limite - p.espera_acumulada
        
        self.chequeo.atender(
            p, duracion_chequeo, self._pasar_a_escaneo,
            callback_inicio=lambda pas, t: setattr(pas, 't_inicio_chequeo', t),
            callback_fin=lambda pas, t: setattr(pas, 't_fin_chequeo', t),
            t_limite_espera=t_restante,
            callback_timeout=self._perdida_vuelo_timeout
        )
        self._programar_llegada()

    def _pasar_a_escaneo(self, p: Pasajero) -> None:
        if p.pierde_vuelo: return
        
        duracion = Distribuciones.exponencial(self.cfg.media_escaneo, self.rng)
        t_restante = self.cfg.tiempo_limite - p.espera_acumulada
        
        self.escaneo.atender(
            p, duracion, self._despues_escaneo,
            callback_inicio=lambda pas, t: setattr(pas, 't_inicio_escaneo', t),
            callback_fin=lambda pas, t: setattr(pas, 't_fin_escaneo', t),
            t_limite_espera=t_restante,
            callback_timeout=self._perdida_vuelo_timeout
        )

    def _despues_escaneo(self, p: Pasajero) -> None:
        if p.pierde_vuelo: return
        
        if Distribuciones.bernoulli(self.cfg.prob_revision, self.rng):
            p.es_revisado = True
            duracion = Distribuciones.exponencial(self.cfg.media_revision, self.rng)
            t_restante = self.cfg.tiempo_limite - p.espera_acumulada
            
            self.revision.atender(
                p, duracion, self._pasar_a_sala,
                callback_inicio=lambda pas, t: setattr(pas, 't_inicio_revision', t),
                callback_fin=lambda pas, t: setattr(pas, 't_fin_revision', t),
                t_limite_espera=t_restante,
                callback_timeout=self._perdida_vuelo_timeout
            )
        else:
            self._pasar_a_sala(p)

    def _pasar_a_sala(self, p: Pasajero) -> None:
        if p.pierde_vuelo: return
        
        t_actual = self.motor.tiempo_actual
        p.t_inicio_sala = t_actual
        espera = Distribuciones.uniforme(self.cfg.espera_sala_min,
                                         self.cfg.espera_sala_max, self.rng)

        def salir_de_sala():
            if p.pierde_vuelo: return
            p.t_fin_sala = self.motor.tiempo_actual

            # Puerta aleatoria
            puerta = self.puerta_a if self.rng.random() < 0.5 else self.puerta_b
            duracion_embarque = Distribuciones.exponencial(self.cfg.media_embarque, self.rng)
            t_restante = self.cfg.tiempo_limite - p.espera_acumulada
            
            puerta.atender(
                p, duracion_embarque, lambda pas: None,
                callback_inicio=lambda pas, t: setattr(pas, 't_inicio_embarque', t),
                callback_fin=lambda pas, t: setattr(pas, 't_fin_embarque', t),
                t_limite_espera=t_restante,
                callback_timeout=self._perdida_vuelo_timeout
            )

        self.motor.programar(t_actual + espera, salir_de_sala)

    @property
    def pasajeros(self) -> list[Pasajero]:
        return self._pasajeros.copy()

    @property
    def utilizacion_escaneo(self) -> float:
        return self.escaneo.utilizacion()

    @property
    def max_cola_escaneo(self) -> int:
        return self.escaneo.max_cola
