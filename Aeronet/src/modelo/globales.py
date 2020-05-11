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
sql3 = "SELECT min(first) FROM caelis.cml_view_installation_interval where station is not null;"
sql4 = "SELECT max(last) FROM caelis.cml_view_installation_interval where station is not null;"
sql5 =  "SELECT C.channel, C.date, avg(C.aod) as aod, min(C.aod) as min, max(C.aod) as max, C.wlc FROM caelis.cml_aod_channel C JOIN caelis.cml_aod A ON (A.ph=C.ph && A.station= %s && A.date=C.date) WHERE (C.ph= %s && C.aod is not null && C.date between %s and %s && (A.cloud_screening_v3!= 'null_values' && A.cloud_screening_v3!= 'notL10')) GROUP BY C.channel, C.date;"
sql51 = "SELECT C.channel, C.date, avg(C.aod) as aod, min(C.aod) as min, max(C.aod) as max, C.wlc FROM caelis.cml_aod_channel C JOIN caelis.cml_aod A ON (A.ph=C.ph && A.station= %s && A.date=C.date) WHERE (C.ph= %s && C.aod is not null && C.date between %s and %s && (A.cloud_screening_v3= 'cloud_free' || A.cloud_screening_v3= 'restoration')) GROUP BY C.channel, C.date;"
sql6 =  "SELECT distinct C.date, C.temp FROM caelis.cml_aod_channel C JOIN caelis.cml_aod A ON (A.ph=C.ph && A.station= %s && A.date=C.date) WHERE (C.ph= %s && C.temp is not null && C.date between %s and %s && (A.cloud_screening_v3!= 'null_values' && A.cloud_screening_v3!= 'notL10')) GROUP BY C.date;"
sql61 = "SELECT distinct C.date, C.temp FROM caelis.cml_aod_channel C JOIN caelis.cml_aod A ON (A.ph=C.ph && A.station= %s && A.date=C.date) WHERE (C.ph= %s && C.temp is not null && C.date between %s and %s && (A.cloud_screening_v3= 'cloud_free' || A.cloud_screening_v3= 'restoration')) GROUP BY C.date;"
sql7 =  "SELECT distinct date, water FROM caelis.cml_aod WHERE (ph= %s && station= %s && water is not null && date between %s and %s && (cloud_screening_v3!= 'null_values' && cloud_screening_v3!= 'notL10')) GROUP BY date;"
sql71 = "SELECT distinct date, water FROM caelis.cml_aod WHERE (ph= %s && station= %s && water is not null && date between %s and %s && (cloud_screening_v3= 'cloud_free' || cloud_screening_v3= 'restoration')) GROUP BY date;"
sql8 = "SELECT distinct date, `alpha_440-870`, `alpha_380-500` FROM caelis.cml_aod WHERE (ph= %s && station= %s && `alpha_380-500` is not null && `alpha_440-870` is not null && date between %s and %s && (cloud_screening_v3!= 'null_values' && cloud_screening_v3!= 'notL10')) GROUP BY date;"
sql81 = "SELECT distinct date, `alpha_440-870`, `alpha_380-500` FROM caelis.cml_aod WHERE (ph= %s && station= %s && `alpha_380-500` is not null && `alpha_440-870` is not null && date between %s and %s && (cloud_screening_v3= 'cloud_free' || cloud_screening_v3= 'restoration')) GROUP BY date;"

sql52 = "select C.channel, C.date, avg(C.aod) as aod, min(C.aod) as min, max(C.aod) as max FROM caelis.cml_aod_channel C JOIN caelis.cml_aod A ON (A.ph=C.ph && A.station= %s && A.date=C.date) WHERE (C.ph= %s && C.aod is not null && C.date between %s and %s) GROUP BY C.channel, C.date;"

#Errores posibles
err1 = "No se estableció conexión con la base de datos"

#Estilo de los canales para su ploteo
fCanalColors = ("", "red", "blue", "cyan", "magenta", "green", "yellow", "orange", "purple", "brown", "black", "turquoise")
fCanalMarkers = ("", "o", "x", "v", "<", ">", "s", "p", "*", "D", "h", "+")