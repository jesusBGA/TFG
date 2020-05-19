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
distinctPhStation =   "SELECT distinct ph, station FROM caelis.cml_view_installation_interval where ((station is not null) && (installation_type in ('master', 'routine', 'calibration')) && ((eprom_type in ('standard', 'extended', 'dualpolar')) || (eprom_subtype in ('analog', 'triple', 'digital')))) order by ph, station;"
distinctPhStationFiltro = "SELECT distinct ph, station FROM caelis.cml_view_installation_interval where ((station is not null) && (installation_type in ('master', 'routine', 'calibration')) && %s) order by ph, station; "
listPhStationDates =  "SELECT  ph, station, first, last, eprom_type, eprom_subtype FROM caelis.cml_view_installation_interval where ((station is not null) && (installation_type in ('master', 'routine', 'calibration')) && ((eprom_type in ('standard', 'extended', 'dualpolar')) || (eprom_subtype in ('analog', 'triple', 'digital')))) order by ph, station;"
listPhStationDatesFiltro = "SELECT  ph, station, first, last, eprom_type, eprom_subtype FROM caelis.cml_view_installation_interval where ((station is not null) && (installation_type in ('master', 'routine', 'calibration')) && (%s)) order by ph, station;"

minFechaFiltroL1 = "select date from caelis.cml_aod where (ph = %s && date >= %s && date <= %s && (cloud_screening_v3!= 'null_values' && cloud_screening_v3!= 'notL10')) order by date ASC limit 1;"
maxFechaFiltroL1 = "select date from caelis.cml_aod where (ph = %s && date <= %s && date >= %s && (cloud_screening_v3!= 'null_values' && cloud_screening_v3!= 'notL10')) order by date DESC limit 1;"
minFechaFiltroL15 = "select date from caelis.cml_aod where (ph = %s && date >= %s && date <= %s && (cloud_screening_v3= 'cloud_free' || cloud_screening_v3= 'restoration')) order by date ASC limit 1;"
maxFechaFiltroL15 = "select date from caelis.cml_aod where (ph = %s && date <= %s && date >= %s && (cloud_screening_v3= 'cloud_free' || cloud_screening_v3= 'restoration')) order by date DESC limit 1;"

minFecha  = "SELECT min(first) FROM caelis.cml_view_installation_interval where ((station is not null) && (installation_type in ('master', 'routine', 'calibration')) && ((eprom_type in ('standard', 'extended', 'dualpolar')) || (eprom_subtype in ('analog', 'triple', 'digital'))));"
minFechaFiltro = "SELECT min(first) FROM caelis.cml_view_installation_interval where (station is not null &&(installation_type in ('master', 'routine', 'calibration')) && %s);"
maxFecha =  "SELECT max(last) FROM caelis.cml_view_installation_interval where ((station is not null) && (installation_type in ('master', 'routine', 'calibration')) && ((eprom_type in ('standard', 'extended', 'dualpolar')) || (eprom_subtype in ('analog', 'triple', 'digital'))));"
maxFechaFiltro = "SELECT max(last) FROM caelis.cml_view_installation_interval where (station is not null &&(installation_type in ('master', 'routine', 'calibration')) && %s);"

aodL1 =  "SELECT C.channel, C.date, avg(C.aod) as aod, min(C.aod) as min, max(C.aod) as max, C.wlc, C.wln FROM caelis.cml_aod_channel C JOIN caelis.cml_aod A ON (A.ph=C.ph && A.station= %s && A.date=C.date) WHERE (C.ph= %s && C.aod is not null && C.date between %s and %s && (A.cloud_screening_v3!= 'null_values' && A.cloud_screening_v3!= 'notL10')) GROUP BY C.channel, C.date;"
aodL15 = "SELECT C.channel, C.date, avg(C.aod) as aod, min(C.aod) as min, max(C.aod) as max, C.wlc, C.wln FROM caelis.cml_aod_channel C JOIN caelis.cml_aod A ON (A.ph=C.ph && A.station= %s && A.date=C.date) WHERE (C.ph= %s && C.aod is not null && C.date between %s and %s && (A.cloud_screening_v3= 'cloud_free' || A.cloud_screening_v3= 'restoration')) GROUP BY C.channel, C.date;"
tempL1 =  "SELECT distinct C.date, C.temp FROM caelis.cml_aod_channel C JOIN caelis.cml_aod A ON (A.ph=C.ph && A.station= %s && A.date=C.date) WHERE (C.ph= %s && C.temp is not null && C.date between %s and %s && (A.cloud_screening_v3!= 'null_values' && A.cloud_screening_v3!= 'notL10')) GROUP BY C.date;"
tempL15 = "SELECT distinct C.date, C.temp FROM caelis.cml_aod_channel C JOIN caelis.cml_aod A ON (A.ph=C.ph && A.station= %s && A.date=C.date) WHERE (C.ph= %s && C.temp is not null && C.date between %s and %s && (A.cloud_screening_v3= 'cloud_free' || A.cloud_screening_v3= 'restoration')) GROUP BY C.date;"
waterL1 =  "SELECT distinct date, water FROM caelis.cml_aod WHERE (ph= %s && station= %s && water is not null && date between %s and %s && (cloud_screening_v3!= 'null_values' && cloud_screening_v3!= 'notL10')) GROUP BY date;"
waterL15 = "SELECT distinct date, water FROM caelis.cml_aod WHERE (ph= %s && station= %s && water is not null && date between %s and %s && (cloud_screening_v3= 'cloud_free' || cloud_screening_v3= 'restoration')) GROUP BY date;"
wExpL1 =  "SELECT distinct date, `alpha_440-870`, `alpha_380-500` FROM caelis.cml_aod WHERE (ph= %s && station= %s && `alpha_380-500` is not null && `alpha_440-870` is not null && date between %s and %s && (cloud_screening_v3!= 'null_values' && cloud_screening_v3!= 'notL10')) GROUP BY date;"
wExpL15 = "SELECT distinct date, `alpha_440-870`, `alpha_380-500` FROM caelis.cml_aod WHERE (ph= %s && station= %s && `alpha_380-500` is not null && `alpha_440-870` is not null && date between %s and %s && (cloud_screening_v3= 'cloud_free' || cloud_screening_v3= 'restoration')) GROUP BY date;"
pwr =  "SELECT C.date, C.M FROM caelis.cml_curvature C WHERE (C.ph= %s && C.M is not null && C.date between %s and %s) GROUP BY C.date;"

#Prueba
sql22 = "SELECT  ph, station, first, last, eprom_type, eprom_subtype FROM caelis.cml_view_installation_interval where ((station is not null) && (installation_type in ('master', 'routine', 'calibration')) && "
sql52 = "select C.channel, C.date, avg(C.aod) as aod, min(C.aod) as min, max(C.aod) as max FROM caelis.cml_aod_channel C JOIN caelis.cml_aod A ON (A.ph=C.ph && A.station= %s && A.date=C.date) WHERE (C.ph= %s && C.aod is not null && C.date between %s and %s) GROUP BY C.channel, C.date;"

#Errores posibles
err1 = "No se estableció conexión con la base de datos"

#Filtros de datos
standard = "eprom_type = 'standard'"
digitalExtended = "eprom_type = 'extended' && eprom_subtype = 'digital'"
triple = "eprom_subtype = 'triple'"
dualpolar = "eprom_type = 'dualpolar' && eprom_subtype != 'triple'"
device = "ph like '%s'"
station = "station like '%s'"


#Estilo de los canales para su ploteo
fCanalColors = ("", "red", "blue", "cyan", "magenta", "green", "yellow", "orange", "purple", "brown", "black", "turquoise")
fCanalMarkers = ("", "o", "x", "v", "<", ">", "s", "p", "*", "D", "h", "d")

COLOR_WLN= { '1640':"#008000", 
            '1240':"#008000",
            '1020':"#ff0000",
            '1020i':"#0000ff",
            '935' : "blue",
            '870' : "#9370db",
            '675':"#556b2f",
            '667':"#606a31",
            '551':"#ff6347",
            '532':"#8b4513",
            '500':"#2e6b57",
            '490':"#2e6b57",
            '443':"#a54141",
            '440':"#a54141",
            '412':"#228b22",
            '380':"#228b22",
            '340':"#b22222"}
