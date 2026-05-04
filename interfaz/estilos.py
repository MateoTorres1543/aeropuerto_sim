"""
Paleta de colores y hoja de estilos global para la interfaz oscura.
"""

COLORES = {
    "fondo":         "#0d1117",
    "superficie":    "#161b22",
    "tarjeta":       "#1c2128",
    "borde":         "#30363d",
    "borde_alto":    "#484f58",
    "acento":        "#2f81f7",
    "exito":         "#3fb950",
    "advertencia":   "#e3b341",
    "peligro":       "#f85149",
    "texto":         "#e6edf3",
    "muted":         "#7d8590",
    "purpura":       "#bc8cff",
}

ESTILO_BASE = f"""
QMainWindow, QWidget {{
    background-color: {COLORES['fondo']};
    color: {COLORES['texto']};
    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial;
    font-size: 13px;
}}

QGroupBox {{
    font-weight: bold;
    border: 1px solid {COLORES['borde']};
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 15px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 5px;
    color: {COLORES['acento']};
}}

QPushButton {{
    background-color: {COLORES['acento']};
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: #478be6;
}}

QPushButton:pressed {{
    background-color: #215bad;
}}

QPushButton:disabled {{
    background-color: {COLORES['borde']};
    color: {COLORES['muted']};
}}

QDoubleSpinBox, QSpinBox, QComboBox {{
    background-color: {COLORES['superficie']};
    border: 1px solid {COLORES['borde']};
    border-radius: 4px;
    padding: 4px;
    color: {COLORES['texto']};
}}

QProgressBar {{
    border: 1px solid {COLORES['borde']};
    border-radius: 4px;
    text-align: center;
    background-color: {COLORES['superficie']};
}}

QProgressBar::chunk {{
    background-color: {COLORES['exito']};
    width: 10px;
}}

QTabWidget::pane {{
    border: 1px solid {COLORES['borde']};
    border-radius: 4px;
    top: -1px;
}}

QTabBar::tab {{
    background-color: {COLORES['superficie']};
    border: 1px solid {COLORES['borde']};
    border-bottom: none;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}}

QTabBar::tab:selected {{
    background-color: {COLORES['tarjeta']};
    border-bottom: 2px solid {COLORES['acento']};
}}

QTableWidget {{
    background-color: {COLORES['superficie']};
    border: 1px solid {COLORES['borde']};
    gridline-color: {COLORES['borde']};
    border-radius: 4px;
}}

QHeaderView::section {{
    background-color: {COLORES['tarjeta']};
    color: {COLORES['muted']};
    padding: 4px;
    border: 1px solid {COLORES['borde']};
    font-weight: bold;
}}
"""
