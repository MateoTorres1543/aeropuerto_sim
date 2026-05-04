import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from interfaz.estilos import ESTILO_BASE, COLORES
from interfaz.ventana_principal import VentanaPrincipal

def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Simulación Aeropuerto")
    app.setStyle("Fusion")
    app.setStyleSheet(ESTILO_BASE)

    paleta = QPalette()
    paleta.setColor(QPalette.ColorRole.Window, QColor(COLORES['fondo']))
    paleta.setColor(QPalette.ColorRole.WindowText, QColor(COLORES['texto']))
    paleta.setColor(QPalette.ColorRole.Base, QColor(COLORES['superficie']))
    paleta.setColor(QPalette.ColorRole.AlternateBase, QColor(COLORES['tarjeta']))
    paleta.setColor(QPalette.ColorRole.ToolTipBase, QColor(COLORES['texto']))
    paleta.setColor(QPalette.ColorRole.ToolTipText, QColor(COLORES['texto']))
    paleta.setColor(QPalette.ColorRole.Text, QColor(COLORES['texto']))
    paleta.setColor(QPalette.ColorRole.Button, QColor(COLORES['superficie']))
    paleta.setColor(QPalette.ColorRole.ButtonText, QColor(COLORES['texto']))
    paleta.setColor(QPalette.ColorRole.BrightText, QColor(COLORES['acento']))
    paleta.setColor(QPalette.ColorRole.Link, QColor(COLORES['acento']))
    paleta.setColor(QPalette.ColorRole.Highlight, QColor(COLORES['acento']))
    paleta.setColor(QPalette.ColorRole.HighlightedText, QColor(COLORES['texto']))
    
    app.setPalette(paleta)

    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
