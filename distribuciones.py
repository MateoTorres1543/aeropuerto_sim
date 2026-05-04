"""
Funciones estáticas para muestrear distribuciones de probabilidad.
Cada función recibe un generador random.Random para reproducibilidad.
"""

import math
import random


class Distribuciones:
    """Namespace de métodos de generación de variables aleatorias."""

    @staticmethod
    def triangular(a: float, m: float, b: float, rng: random.Random) -> float:
        """Distribución Triangular(a, m, b)."""
        # Validar que los parámetros sean correctos para evitar errores internos de random
        low, mode, high = sorted([a, m, b])
        return rng.triangular(low, high, mode)

    @staticmethod
    def exponencial(media: float, rng: random.Random) -> float:
        """Distribución Exponencial con la media dada."""
        # Evitar división por cero si la media es 0
        if media <= 0:
            return 0.0001 
        return rng.expovariate(1.0 / media)

    @staticmethod
    def bernoulli(p: float, rng: random.Random) -> bool:
        """Verdadero con probabilidad p."""
        return rng.random() < p

    @staticmethod
    def uniforme(a: float, b: float, rng: random.Random) -> float:
        """Distribución Uniforme(a, b)."""
        low, high = min(a, b), max(a, b)
        if low == high:
            return low
        return rng.uniform(low, high)
