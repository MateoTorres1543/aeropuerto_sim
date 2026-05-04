from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QBrush, QFont, QPainterPath, QColor
from .estilos import COLORES

class DiagramaFlujo(QWidget):
    """
    Widget que dibuja un diagrama de flujo del proceso aeroportuario.
    Se actualiza reactivamente según los parámetros.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(220)
        self.num_mostradores = 3
        self.num_escaneres = 3
        self.num_agentes = 2

    def actualizar(self, mostradores, escaneres, agentes):
        self.num_mostradores = mostradores
        self.num_escaneres = escaneres
        self.num_agentes = agentes
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w, h = self.width(), self.height()
        # Asegurar un tamaño mínimo para el dibujo
        escala = min(w / 800.0, h / 200.0, 1.2)
        painter.scale(escala, escala)

        fuente = QFont("Segoe UI", 9, QFont.Weight.Bold)
        painter.setFont(fuente)

        # Configuración de cajas
        ancho_caja, alto_caja = 110, 50
        y_centrado = 60
        espaciado_x = 150

        pasos = [
            (50,  y_centrado, "Llegadas",  COLORES['texto']),
            (50 + espaciado_x, y_centrado, f"Chequeo\n({self.num_mostradores})", COLORES['purpura']),
            (50 + 2*espaciado_x, y_centrado, f"Escáneres\n({self.num_escaneres})", COLORES['acento']),
            (50 + 3*espaciado_x, y_centrado - 40, f"Revisión\n({self.num_agentes})", COLORES['advertencia']),
            (50 + 3*espaciado_x, y_centrado + 40, "Sala Espera", COLORES['exito']),
            (50 + 4*espaciado_x, y_centrado + 40, "Embarque", COLORES['exito']),
        ]

        # Dibujar flechas primero
        pen_flecha = QPen(QColor(COLORES['borde_alto']), 2)
        painter.setPen(pen_flecha)
        
        # Conexiones (Llegada -> Chequeo -> Escaneo)
        self._dibujar_flecha(painter, 160, y_centrado + 25, 190, y_centrado + 25)
        self._dibujar_flecha(painter, 310, y_centrado + 25, 340, y_centrado + 25)
        
        # Escaneo -> Revisión o Sala
        self._dibujar_flecha(painter, 460, y_centrado + 15, 495, y_centrado - 15) # a revisión
        self._dibujar_flecha(painter, 460, y_centrado + 35, 495, y_centrado + 55) # a sala
        
        # Revisión -> Sala
        self._dibujar_flecha(painter, 555, y_centrado + 10, 555, y_centrado + 35)
        
        # Sala -> Embarque
        self._dibujar_flecha(painter, 610, y_centrado + 65, 645, y_centrado + 65)

        # Dibujar cajas
        for x, y, texto, color in pasos:
            rect = QRectF(x, y, ancho_caja, alto_caja)
            
            # Sombra
            painter.setBrush(QBrush(QColor(0, 0, 0, 80)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect.translated(2, 2), 6, 6)

            # Caja
            painter.setBrush(QBrush(QColor(COLORES['tarjeta'])))
            painter.setPen(QPen(QColor(color), 2))
            painter.drawRoundedRect(rect, 6, 6)

            # Texto
            painter.setPen(QPen(QColor(COLORES['texto'])))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, texto)

    def _dibujar_flecha(self, painter, x1, y1, x2, y2):
        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        # Cabeza de flecha
        path = QPainterPath()
        path.moveTo(x2, y2)
        path.lineTo(x2 - 8, y2 - 4)
        path.lineTo(x2 - 8, y2 + 4)
        path.closeSubpath()
        painter.setBrush(QBrush(QColor(COLORES['borde_alto'])))
        painter.drawPath(path)
