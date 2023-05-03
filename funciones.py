import plotly.express  as px
import numpy as np

def qaqc(original, control, error, warning):
    valor = ((abs(original - control )/original)*100)
    if valor >= error:
        return 'Error'
    elif valor >= warning:
        return 'Advertencia'
    else:
        return 'OK'

def grafico(df, charttype, error, warning, ancho, alto):
    if charttype == 'Scatter':
        fig = px.scatter(data_frame=df, x="ASSAYVALUE_OR", y="ASSAYVALUE_CK",  color='QAQC',color_discrete_map={'OK':'blue', 'Advertencia':'orange', 'Error':'red'})
        fig.update_layout(title="QAQC", xaxis_title="Original", yaxis_title="Check", width=ancho, height=alto)

        # Agrega una línea x=y al gráfico
        linea_xy = {'type': 'line', 'x0': df['ASSAYVALUE_OR'].min(), 'y0': df['ASSAYVALUE_OR'].min(), 'x1': df['ASSAYVALUE_OR'].max(), 'y1': df['ASSAYVALUE_OR'].max()}
        linea_pwar  = {'type': 'line', 'x0': df['ASSAYVALUE_OR'].min(), 'y0': (df['ASSAYVALUE_OR'].min()+((warning/100)*df['ASSAYVALUE_OR'].min())), 'x1': df['ASSAYVALUE_OR'].max(), 'y1': (df['ASSAYVALUE_OR'].max()+((warning/100)*df['ASSAYVALUE_OR'].max()))}
        linea_mwar  = {'type': 'line', 'x0': df['ASSAYVALUE_OR'].min(), 'y0': (df['ASSAYVALUE_OR'].min()-((warning/100)*df['ASSAYVALUE_OR'].min())), 'x1': df['ASSAYVALUE_OR'].max(), 'y1': (df['ASSAYVALUE_OR'].max()-((warning/100)*df['ASSAYVALUE_OR'].max()))}
        linea_perr  = {'type': 'line', 'x0': df['ASSAYVALUE_OR'].min(), 'y0': (df['ASSAYVALUE_OR'].min()+((error/100)*df['ASSAYVALUE_OR'].min())), 'x1': df['ASSAYVALUE_OR'].max(), 'y1': (df['ASSAYVALUE_OR'].max()+((error/100)*df['ASSAYVALUE_OR'].max()))}
        linea_merr  = {'type': 'line', 'x0': df['ASSAYVALUE_OR'].min(), 'y0': (df['ASSAYVALUE_OR'].min()-((error/100)*df['ASSAYVALUE_OR'].min())), 'x1': df['ASSAYVALUE_OR'].max(), 'y1': (df['ASSAYVALUE_OR'].max()-((error/100)*df['ASSAYVALUE_OR'].max()))}
        fig.add_shape(linea_xy, line={'dash': 'dash', 'color': 'grey', 'width': 0.8})
        fig.add_shape(linea_pwar, line={'dash': 'dash', 'color': 'orange', 'width': 0.8})
        fig.add_shape(linea_mwar, line={'dash': 'dash', 'color': 'orange', 'width': 0.8})
        fig.add_shape(linea_perr, line={'dash': 'dash', 'color': 'red', 'width': 0.8})
        fig.add_shape(linea_merr, line={'dash': 'dash', 'color': 'red', 'width': 0.8})

    elif charttype == 'RD v Mean Grade':
        fig = px.scatter(data_frame=df, x="Media", y="MPRD", color='QAQC',color_discrete_map={'OK':'blue', 'Advertencia':'orange', 'Error':'red'})
        fig.update_layout(title="QAQC", xaxis_title="Mean", yaxis_title="MPRD", width=ancho, height=alto)
        linea_xy = {'type': 'line', 'x0': df['Media'].min(), 'y0': 0, 'x1': df['Media'].max(), 'y1': 0}
        linea_pwar  = {'type': 'line', 'x0': df['Media'].min(), 'y0': warning, 'x1': df['Media'].max(), 'y1': warning}
        linea_mwar =  {'type': 'line', 'x0': df['Media'].min(), 'y0': warning*-1, 'x1': df['Media'].max(), 'y1': warning*-1}
        linea_perr =  {'type': 'line', 'x0': df['Media'].min(), 'y0': error, 'x1': df['Media'].max(), 'y1': error}
        linea_merr = {'type': 'line', 'x0': df['Media'].min(), 'y0': error*-1, 'x1': df['Media'].max(), 'y1': error*-1}
        fig.add_shape(linea_xy, line={'dash': 'dash', 'color': 'grey', 'width': 0.8})
        fig.add_shape(linea_pwar, line={'dash': 'dash', 'color': 'orange', 'width': 0.8})
        fig.add_shape(linea_mwar, line={'dash': 'dash', 'color': 'orange', 'width': 0.8})
        fig.add_shape(linea_perr, line={'dash': 'dash', 'color': 'red', 'width': 0.8})
        fig.add_shape(linea_merr, line={'dash': 'dash', 'color': 'red', 'width': 0.8})
   
    elif charttype == 'ARD v Mean Grade':
        fig = px.scatter(data_frame=df, x="Media", y="AMPRD", color='QAQC',color_discrete_map={'OK':'blue', 'Advertencia':'orange', 'Error':'red'})
        fig.update_layout(title="QAQC", xaxis_title="Mean", yaxis_title="AMPRD", width=ancho, height=alto)
        linea_xy = {'type': 'line', 'x0': df['Media'].min(), 'y0': 0, 'x1': df['Media'].max(), 'y1': 0}
        linea_pwar  = {'type': 'line', 'x0': df['Media'].min(), 'y0': warning, 'x1': df['Media'].max(), 'y1': warning}
        linea_perr =  {'type': 'line', 'x0': df['Media'].min(), 'y0': error, 'x1': df['Media'].max(), 'y1': error}
        fig.add_shape(linea_xy, line={'dash': 'dash', 'color': 'grey', 'width': 0.8})
        fig.add_shape(linea_pwar, line={'dash': 'dash', 'color': 'orange', 'width': 0.8})
        fig.add_shape(linea_perr, line={'dash': 'dash', 'color': 'red', 'width': 0.8})
       
    
    return fig

def stats(col1: float, col2: float, tipo: str) -> float:
    if tipo == 'mean':
        resultado = np.mean([col1, col2])
    elif tipo == 'mprd':
        resultado = ((col1 - col2) / np.mean([col1, col2])) * 100        
    elif tipo == 'amprd':
        resultado = (np.abs(col1 - col2) / np.mean([col1, col2])) * 100
    return f"{resultado:.2f}"