# from sqlalchemy import create_engine
import pandas as pd
from urllib.parse import quote
from datetime import datetime as dt
import plotly.graph_objects as go
import plotly.express  as px
import numpy as np
from funciones import stats

# engine=create_engine('mssql+pyodbc://'+dbuser+':'+quote(dbpassword)+'@'+dbserver+'/'+dbname+'?driver=ODBC+Driver+17+for+SQL+Server',fast_executemany=True)

# consultaqaqc = "select * from QV_QC_CORP_DRILLHOLE_BASE_OR_C"
# dfqaqc1=pd.read_sql(consultaqaqc, con=engine)
# dfqaqc1.to_csv('datosqaqc111.csv', index=False)


dfqaqc = pd.read_csv('datosqaqc.csv', sep=',')


dfdups = dfqaqc[['ASSAYNAME','ID_OR','ASSAYVALUE_OR','DUPLICATENO_OR','ID_CK','ASSAYVALUE_CK','DUPLICATENO_CK', 'CHECKSTAGE_CK', 'RETURNDATE_CK', 'DESPATCHNO_CK','LABCODE_CK','LABJOBNO_CK']]
dfdups = dfdups.assign(
    Media=dfdups.apply(lambda x: float(stats(x['ASSAYVALUE_OR'], x['ASSAYVALUE_CK'], 'mean')), axis=1),
    MPRD=dfdups.apply(lambda x: float(stats(x['ASSAYVALUE_OR'], x['ASSAYVALUE_CK'], 'mprd')), axis=1),
    AMPRD=dfdups.apply(lambda x: float(stats(x['ASSAYVALUE_OR'], x['ASSAYVALUE_CK'], 'amprd')), axis=1),
    FechaACQ = pd.to_datetime(dfdups['RETURNDATE_CK']).dt.strftime('%d-%b-%Y'),
    RETURNDATE_CK = pd.to_datetime(dfdups['RETURNDATE_CK'])    
)

def basededatos():
    return dfdups
