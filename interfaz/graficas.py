from PyQt6.QtCharts import (
    QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis,
    QValueAxis, QLineSeries
)
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt
from .estilos import COLORES

def construir_histograma(datos: list[float], titulo: str, color_barras: str) -> QChartView:
    chart = QChart()
    chart.setTitle(titulo)
    chart.setBackgroundVisible(False)
    chart.setTitleBrush(QColor(COLORES['texto']))
    
    # Crear bins simples
    if not datos:
        return QChartView(chart)
        
    min_val, max_val = min(datos), max(datos)
    num_bins = 15
    ancho_bin = (max_val - min_val) / num_bins if max_val > min_val else 1
    
    bins = [0] * num_bins
    for x in datos:
        idx = min(int((x - min_val) / ancho_bin), num_bins - 1)
        bins[idx] += 1
        
    set_barras = QBarSet("Pasajeros")
    set_barras.append(bins)
    set_barras.setColor(QColor(COLORES[color_barras]))
    set_barras.setBorderColor(QColor(COLORES['tarjeta']))
    
    series = QBarSeries()
    series.append(set_barras)
    chart.addSeries(series)
    
    axis_x = QBarCategoryAxis()
    categorias = [f"{min_val + i*ancho_bin:.1f}" for i in range(num_bins)]
    axis_x.append(categorias)
    axis_x.setLabelsColor(QColor(COLORES['muted']))
    chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
    series.attachAxis(axis_x)
    
    axis_y = QValueAxis()
    axis_y.setLabelFormat("%d")
    axis_y.setLabelsColor(QColor(COLORES['muted']))
    chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
    series.attachAxis(axis_y)
    
    chart.legend().hide()
    
    view = QChartView(chart)
    view.setRenderHint(QPainter.RenderHint.Antialiasing)
    view.setMinimumHeight(300)
    return view

def construir_convergencia(replicas: list, titulo: str) -> QChartView:
    chart = QChart()
    chart.setTitle(titulo)
    chart.setBackgroundVisible(False)
    chart.setTitleBrush(QColor(COLORES['texto']))
    
    series = QLineSeries()
    series.setName("Media acumulada")
    
    suma = 0
    for i, r in enumerate(replicas):
        suma += r.media_espera
        series.append(i + 1, suma / (i + 1))
        
    pen = series.pen()
    pen.setWidth(3)
    pen.setColor(QColor(COLORES['acento']))
    series.setPen(pen)
    
    chart.addSeries(series)
    chart.createDefaultAxes()
    
    if chart.axes():
        chart.axes(Qt.Orientation.Horizontal)[0].setLabelsColor(QColor(COLORES['muted']))
        chart.axes(Qt.Orientation.Vertical)[0].setLabelsColor(QColor(COLORES['muted']))
    
    view = QChartView(chart)
    view.setRenderHint(QPainter.RenderHint.Antialiasing)
    view.setMinimumHeight(300)
    return view
