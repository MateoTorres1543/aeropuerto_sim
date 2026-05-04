from PyQt6.QtCore import QThread, pyqtSignal
from configuracion import ConfiguracionEscenario, ParametrosEjecucion
from simulador import Simulador


class HiloSimulacion(QThread):
    progreso = pyqtSignal(int, int)
    terminado = pyqtSignal(object)      # ResultadoEscenario
    error = pyqtSignal(str)

    def __init__(self, cfg: ConfiguracionEscenario, params: ParametrosEjecucion) -> None:
        super().__init__()
        self._cfg = cfg
        self._params = params

    def run(self) -> None:
        try:
            sim = Simulador(self._cfg, self._params)
            resultado = sim.ejecutar(callback_progreso=self._reportar_progreso)
            self.terminado.emit(resultado)
        except Exception as e:
            self.error.emit(str(e))

    def _reportar_progreso(self, actual: int, total: int) -> None:
        self.progreso.emit(actual, total)
