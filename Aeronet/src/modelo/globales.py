'''
Created on 28 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''

#Conexión base de datos
database_host = "www.caelis.uva.es"
database_name = "caelis"
user = "curioso"
password = "tupadre"

#Consultas a la bbdd
sql1 = "SELECT distinct ph, station FROM caelis.cml_view_installation_interval where station is not null"
sql2 = "SELECT  ph, station, first, last, eprom_type, eprom_subtype FROM caelis.cml_view_installation_interval where ((station is not null) && (installation_type in ('master', 'routine', 'calibration')) && ((eprom_type in ('standard', 'extended', 'dualpolar')) || (eprom_subtype in ('analog', 'triple')))) order by ph, station;"
sql3 = "SELECT min(first) FROM caelis.cml_view_installation_interval;"
sql4 = "SELECT max(last) FROM caelis.cml_view_installation_interval;"
sql5 = "SELECT select C.channel, C.date, avg(C.aod) from caelis.cml_aod_channel C join caelis.cml_aod A on (A.ph=C.ph && A.date=C.date) where (C.ph=%s && C.aod is not null) group by C.channel, C.date;"

#Errores posibles
err1 = "No se estableció conexión con la base de datos"