#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------------
# Laboratorio de Datos - TP 1
# Limpieza, manejo y visualización de datos
# Autores: Altamirano Ailen, Rio Francisco, Ruz Veloso Luciano
# --------------------------------------------------------------
# ********************** las_yararas ***************************
#%%
# Importamos bibliotecas necesarias
import pandas as pd
from inline_sql import sql, sql_val
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
#%%
# Importamos archivos necesarios
padron = pd.read_csv("./padron-de-operadores-organicos-certificados.csv", index_col=0, encoding='latin-1')
salarios = pd.read_csv("./w_median_depto_priv_clae2.csv")
localidades = pd.read_csv("./localidades-censales.csv")
dicc_deptos = pd.read_csv("./diccionario_cod_depto.csv")
dicc_clases = pd.read_csv("./diccionario_clae2.csv")
rubro_clae = pd.read_csv("./Rubro_clae .csv")

#%%
# DEFINICION DE FUNCIONES

print(padron.shape)

def separar1FN(data, columna, separador):
    """
    Función que recibe un dataFrame de pandas con una columna
    llamada id_registro, el nombre de una columna (str)
    y un separador (str). Devuelve un dataframe de dos columnas: id_registro
    y la columna deseada, ahora conteniendo valores atómicos.
    La función es util para tratar tablas que no estan en primera forma normal.
    """
    # Creamos un diccionario vacío para almacenar los resultados
    dict_separar_data = {'id_registro': [], columna:[]}

    # Itera por cada registro en el df
    for i in range(len(data)):
        # Obtenemos la cadena de valores del registro actual
        columna_str = data.iloc[i][columna]

        # Checkeamos si la cadena de valores es un null
        if pd.isnull(columna_str) or columna_str == '':
            columna_list = []
        else:
            # Separamos los valores en una lista utilizando el separador especificado
            columna_list = columna_str.split(separador)

        for valor in columna_list:
            dict_separar_data['id_registro'].append(data.iloc[i]['id_registro'])
            dict_separar_data[columna].append(valor)

    # Creamos un nuevo df a partir del diccionario
    data_separada = pd.DataFrame(dict_separar_data)

    return data_separada
#%%
## Proceso de limpieza y calidad de los datos
    
# ADAPTACIÓN DE LA TABLA PADRON PARA QUE SE ENCUENTRE EN 1FN
# Le agregamos una columna id a la tabla padrón y renombramos columna razon_social

id_registro = [i for i in range(padron.shape[0])]
padron['id_registro'] = id_registro
padron.rename(columns={'razón social':'razon_social'},inplace=True)

# Separamos la columna productos del df padron
lista_separadores = [', ',' Y ','?','-',' + ']
productos = padron
columna = 'productos'

for separador in lista_separadores:
    productos = separar1FN(productos, columna, separador)


# Separamos rubros en padron
lista_separadores = ['/',';']
rubro = padron
columna = 'rubro'

for separador in lista_separadores:
    rubro = separar1FN(rubro, columna, separador)

#%%
# Eliminamos tildes y cambiamos a mayúsculas en localidades
localidades =        sql^ """
                    SELECT *, UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
                    departamento_nombre, 'á', 'a'), 'é', 'e'), 'í', 'i')
                    , 'ó', 'o'), 'ú', 'u'))AS departamento_nombre
                    FROM localidades
                    """
localidades

# Eliminamos tildes y cambiamos a mayúsculas en dicc_deptos
dicc_deptos =        sql^ """
                    SELECT *, UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
                    nombre_departamento_indec, 'á', 'a'), 'é', 'e'), 'í', 'i')
                    , 'ó', 'o'), 'ú', 'u'))AS nombre_departamento_indec
                    FROM dicc_deptos
                    """
dicc_deptos


# Eliminamos tildes y pasamos a mayusculas en la columna dicc_deptos
dicc_deptos =        sql^ """
                    SELECT *, UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
                    nombre_provincia_indec, 'á', 'a'), 'é', 'e'), 'í', 'i')
                    , 'ó', 'o'), 'ú', 'u'))AS nombre_provincia_indec
                    FROM dicc_deptos
                    """
dicc_deptos

# Eliminamos tildes y pasamos a mayusculas en la columna provincia de localidades
localidades =        sql^ """
                    SELECT *, REPLACE(UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
                   provincia_nombre, 'á', 'a'), 'é', 'e'), 'í', 'i')
                    , 'ó', 'o'), 'ú', 'u')), 'TIERRA DEL FUEGO, ANTARTIDA E ISLAS DEL ATLANTICO SUR',
                    'TIERRA DEL FUEGO')
                    AS provincia_nombre,
                    UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(municipio_nombre,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u')) AS municipio_nombre,
                    UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(nombre,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u')) AS nombre,

                    FROM localidades
                    """
localidades

# Armamos tabla departamentos a partir del padron con consultas SQL
departamento = sql^ """
                    SELECT codigo_departamento_indec, nombre_departamento_indec, id_provincia_indec
                    FROM dicc_deptos
                    """
departamento

# Armamos tabla certificadora a partir del padron con consultas SQL
certificadora = sql^ """
                    SELECT DISTINCT Certificadora_id, certificadora_deno
                    FROM padron
                    """
certificadora

# Armamos tabla categoria a partir del padron con consultas SQL
categoria =    sql^ """
                    SELECT DISTINCT categoria_id, categoria_desc
                    FROM padron
                    """
categoria

# Armamos tabla provincia a partir del padron con consultas SQL
provincia =    sql^ """
                    SELECT DISTINCT provincia_id, provincia_nombre_2
                    FROM localidades
                    """
provincia

# Armamos tabla clases a partir del padron con consultas SQL
clases =       sql^ """
                    SELECT DISTINCT clae2, clae2_desc, letra
                    FROM dicc_clases
                    """
clases

# Armamos tabla letra a partir del padron con consultas SQL
letra =        sql^ """
                    SELECT DISTINCT letra, letra_desc
                    FROM dicc_clases
                    """
letra


# Eliminar columnas del padron de operadores organicos para que este en 3FN
padron =        sql^ """
                    SELECT DISTINCT id_registro, provincia_id, departamento,
                    localidad, categoria_id, Certificadora_id, razon_social,
                    establecimiento
                    FROM padron
                    """
padron

#Armo la tabla municipio
municipio = sql^"""
SELECT DISTINCT municipio_id,municipio_nombre_2, departamento_id
FROM localidades
"""
departamento_localidades = sql^"""
SELECT DISTINCT departamento_id,departamento_nombre_2
FROM localidades
"""
#Selecciono las columnas correspondientes en localidades para que este en 1FN
#Eliminamos la columna fuente pues es todo INDEC
localidades= sql^"""
SELECT categoria,centroide_lat,centroide_lon,departamento_id,funcion,id,
municipio_id,nombre_2,provincia_id
FROM localidades
"""
#%%

# Agregamos el codigo correspondiente a CABA en localidades
localidades.loc[localidades['nombre_2'] == 'CIUDAD AUTONOMA DE BUENOS AIRES', 'departamento_id'] = 2000

# Corregimos el nombre de CABA en padron para que sea igual a localidades
padron.loc[padron['departamento'] == 'CIUDAD AUTONOMA BUENOS AIRES', 'departamento'] = 'CIUDAD AUTONOMA DE BUENOS AIRES'


#Eliminamos en padron los rubro SIN DEFINIR
print("Padron contando rubro SIN DEFINIR:",padron.shape)
padron = sql ^ """
SELECT DISTINCT p.*
FROM padron AS p
JOIN rubro AS r
ON p.id_registro = r.id_registro
WHERE r.rubro != 'SIN DEFINIR'
"""
print("Padron sin contar rubro SIN DEFINIR:",padron.shape)

# Chequeamos inconsistencias de id provincias entre las 3 tablas
# En dicc_depto
Depto = """
SELECT DISTINCT dd.id_provincia_indec,dd.nombre_provincia_indec_2
FROM dicc_deptos AS dd
LEFT OUTER JOIN dicc_deptos AS dd2
ON dd.nombre_provincia_indec_2 = dd2.nombre_provincia_indec_2
WHERE dd.id_provincia_indec != dd2.id_provincia_indec
"""
print("Errores en departamento:",(sql^ Depto).shape)

# Entre dicc_depto y padron de operadores
Depto_PadronOpOrg = """
SELECT DISTINCT poo.provincia_id,poo.provincia_nombre_2,dd.id_provincia_indec,dd.nombre_provincia_indec_2
FROM provincia AS poo
LEFT OUTER JOIN dicc_deptos AS dd
ON poo.provincia_nombre_2 = dd.nombre_provincia_indec_2
WHERE poo.provincia_id != dd.id_provincia_indec
"""
print("Errores en padron:",(sql^ Depto_PadronOpOrg).shape)

# Entre dicc_depto y localidades
localidades_join = sql^ """
SELECT DISTINCT l.*, p.provincia_nombre_2
FROM localidades AS l
JOIN provincia AS p
ON p.provincia_id = l.provincia_id
"""

Depto_LocSensales = """
SELECT DISTINCT dd.id_provincia_indec,dd.nombre_provincia_indec_2
FROM dicc_deptos AS dd
LEFT OUTER JOIN localidades_join AS lc
ON dd.nombre_provincia_indec_2 = lc.provincia_nombre_2
WHERE dd.id_provincia_indec != lc.provincia_id
"""
print("Errores en localidades:",(sql^ Depto_LocSensales).shape)

# Comparamos el diccionario de departamentos con la informacion de localidades
# censales de indec. Los códigos de departamentos deben ser consistentes entre tablas

# Unimos las tablas por nombre de departamento y provincia
# comparamos los codigos de departamentos de cada tabla

localidades_join = sql^ """
SELECT DISTINCT l.*, d.departamento_nombre_2
FROM localidades_join AS l
JOIN departamento_localidades AS d
ON d.departamento_id = l.departamento_id
"""

Depto = sql^"""
SELECT DISTINCT dd.codigo_departamento_indec,loc.departamento_id,	dd.nombre_departamento_indec_2
FROM dicc_deptos AS dd
LEFT OUTER JOIN localidades_join AS loc
ON dd.nombre_departamento_indec_2 = loc.departamento_nombre_2 AND dd.nombre_provincia_indec_2 = loc.provincia_nombre_2
WHERE dd.codigo_departamento_indec != loc.departamento_id OR dd.id_provincia_indec != loc.provincia_id
"""

print(f'n departamentos código distinto/ n departamentos de dicc_deptos: {Depto.shape[0]/ dicc_deptos.shape[0]}')
print(Depto)
# hay que corregir el caso de USHUAIA
# El codigo 'real' es el de localidades censales

dicc_deptos[dicc_deptos['codigo_departamento_indec']==94014]
# El codigo de departamento 94014 aparece solo una vez, asi que lo
# podemos reemplazar
dicc_deptos.loc[dicc_deptos['codigo_departamento_indec']==94014, 'codigo_departamento_indec'] = 94015
# Checkeo el reemplazo, no debería aparecer el codigo 94014
dicc_deptos[dicc_deptos['codigo_departamento_indec']==94014]
dicc_deptos[dicc_deptos['codigo_departamento_indec']==94015]


# Unimos las tablas segun los codigos de departamento y provincia
# comparamos los nombres de departamentos en los casos que los codigos
# coinciden. Los nombres deberían ser consistentes entre tablas.
Depto = sql^ """
SELECT DISTINCT dd.codigo_departamento_indec, dd.nombre_departamento_indec_2, loc.departamento_nombre_2
FROM dicc_deptos AS dd
LEFT OUTER JOIN localidades_join AS loc
ON dd.codigo_departamento_indec = loc.departamento_id AND dd.id_provincia_indec = loc.provincia_id
WHERE dd.nombre_departamento_indec_2 != loc.departamento_nombre_2 OR dd.nombre_provincia_indec_2 != loc.provincia_nombre_2
"""

print(f'n departamentos nombre distinto/ n departamentos de dicc_deptos: {Depto.shape[0]/ dicc_deptos.shape[0]}')
print(Depto)
# Hay 9 casos que solucionar
# Uso el dataframe resultante de la consulta para reemplazar los nombres
# en la tabla dicc_deptos
for i,codigo in enumerate(Depto['codigo_departamento_indec']):
    dicc_deptos.loc[dicc_deptos['codigo_departamento_indec']==codigo,
                    'nombre_departamento_indec_2'] = Depto.loc[i, 'departamento_nombre_2']

#Chequeo que los departamentos de padron esten incluidos en localidades
#print("Cantidad de localidades",localidades_join.shape)
localidades_join = sql^ """
SELECT DISTINCT l.*, m.municipio_nombre_2
FROM localidades_join AS l
LEFT JOIN municipio AS m
ON l.municipio_id = m.municipio_id"""
#print("Cantidad de localidades",localidades_join.shape)
#Si usamos JOIN eliminamos los departamentos sin localidad, preferimos dejarlos.

col1_df1 = padron['departamento']
col1_df2 = localidades_join['departamento_nombre_2']
col2_df2 = localidades_join['municipio_nombre_2']
col3_df2 = localidades_join['nombre_2']

valores_unicos_df1 = set(col1_df1)
valores_unicos_c1_df2 = set(col1_df2)
valores_unicos_c2_df2 = set(col2_df2)
valores_unicos_c3_df2 = set(col3_df2)

valores_en_df1 = valores_unicos_df1.difference(valores_unicos_c1_df2)
valores_en_df1 = valores_en_df1.difference(valores_unicos_c3_df2)

#i=0
#for departamento in col1_df1:
#  if departamento in valores_en_df1:
#    i+=1
#print("Nombres de departamentos que no estan en localidades: ",i,"/",len(col1_df1))
# hay 156 departamentos en padron que no corresponden a nombres de departamento,
# municipio o localidad en localidades censales.
# Usar sets para evaluar esto tiene una limitación, solamente comparamos nombres de
# departamentos, y no tenemos en cuenta que podría haber dos departamentos con el
# mismo nombre en provincias distintas.


# Agregamos el nombre de provincia en padron
padron_provincia=sql^"""
SELECT DISTINCT p.*, prov.provincia_nombre_2 AS provincia
FROM padron as p
INNER JOIN provincia AS prov
ON p.provincia_id = prov.provincia_id
"""

# A cada departamento en padron le asignamos su codigo correspondiente con departamento en localidades
padron = sql^"""
SELECT DISTINCT p.*, loc.departamento_id
FROM padron_provincia as p
LEFT OUTER JOIN localidades_join AS loc
ON p.departamento = loc.departamento_nombre_2 AND p.provincia = loc.provincia_nombre_2
"""

# A cada departamento en padron le asignamos su codigo correspondiente con nombre en localidades
padron = sql^"""
SELECT DISTINCT p.id_registro, p.provincia_id, p.departamento,
                    p.localidad, p.categoria_id, p.Certificadora_id, p.razon_social,
                    p.establecimiento, loc.departamento_id,p.departamento_id
FROM padron as p
LEFT OUTER JOIN localidades_join AS loc
ON p.departamento = loc.nombre_2 AND p.provincia = loc.provincia_nombre_2 AND p.departamento_id IS NULL
"""

# Reemplazamos los Na por 0
padron['departamento_id'] = padron['departamento_id'].fillna(0)
padron['departamento_id_2'] = padron['departamento_id_2'].fillna(0)

# A partir de la suma de las columnas obtenemos los ids
padron['departamento_id_3']=padron['departamento_id']+padron['departamento_id_2']

#vemos si hay localilades con dos departamentos distintos en la misma provincia(tuplas espureas)
padron['id_registro'].value_counts()
padron[padron['id_registro']==983]
padron[padron['id_registro']==10]

#Los eliminamos
filtro = padron['departamento'] != 'LOS CARDALES'
padron = padron[filtro]

# Asigno el codigo de departamento correspondiente a CABA
padron.loc[padron['departamento'] == 'CIUDAD AUTONOMA DE BUENOS AIRES', 'departamento_id_3'] = 2000
print(padron[padron['departamento_id_3']== 2000][['departamento', 'departamento_id_3']])


# Veo cuantos nulls quedaron finalmente en la columna departamento_id_3
print('Antes de corregir los departamentos que son localidades:\n')
print(sql^"""
SELECT count(*) AS departamentos_sin_codigo
FROM padron
WHERE departamento_id = 0
""")
print('\nDespues de la corrección:\n')
print(sql^"""
SELECT count(*) AS departamentos_sin_codigo
FROM padron
WHERE departamento_id_3 = 0
""")


# Decidimos eliminar los registros a los que no les podemos asignar un codigo de departamento

print("Cantidad de operadores antes: ",padron.shape)
padron = sql^"""
SELECT DISTINCT p.id_registro, p.provincia_id, p.departamento,
                    p.localidad, p.categoria_id, p.Certificadora_id, p.razon_social,
                    p.establecimiento, p.departamento_id_3
FROM padron as p
WHERE p.departamento_id_3 != 0
"""
print("Cantidad de operadores despues:",padron.shape)


# Limpieza de los datos de salarios
print(salarios['w_median'].value_counts())
print(salarios.shape)

# Le asignamos Na a los valores -99
salarios[salarios['w_median'] == -99] = np.nan

# Checkeo que no haya -99
salarios['w_median'].value_counts()
salarios[salarios['w_median'] == -99]

# Queremos que todos los registros de salario tengan fecha
# cuantos registros hay que tengan na en fecha
salarios['fecha'].isna().sum()

# Decidimos eliminar estos registros
salarios = salarios.dropna(subset=['fecha'])
salarios['fecha'].isna().sum()

###################################################################
#%%
# pregunta i
# ¿Existen provincias que no presentan Operadores Orgánicos Certificados?
# ¿En caso de que sí, cuántas y cuáles son?

# Revisamos que provincias no tienen operadores
provincias_con_operadores = sql^"""
SELECT DISTINCT provincia_id
FROM padron
"""
provincias_sin_operadores = sql^"""
SELECT DISTINCT *,
FROM provincia as p
LEFT OUTER JOIN provincias_con_operadores as po
ON p.provincia_id = po.provincia_id
WHERE po.provincia_id IS NULL
"""
print("Provincias sin operadores: ",provincias_sin_operadores.shape)
# No hay provincias sin operadores, solo aparecen el caso de eliminar
# los operadores sin localidades.

# ii
# Revisamos que departamento no tienen operadores
departamentos_sin_operadores = sql^"""
SELECT DISTINCT l.departamento_nombre_2, l.departamento_id
FROM localidades_join AS l
LEFT OUTER JOIN padron AS p
ON p.provincia_id = l.provincia_id AND l.departamento_id = p.departamento_id_3
WHERE p.id_registro IS NULL
"""
departamentos_sin_operadores.shape
# Hay 311 departamentos sin operadores

# TEST consulta ii
# Revisamos que Avellaneda este en departamentos_sin_operadores y no en padron
#departamentos_sin_operadores[departamentos_sin_operadores['departamento_nombre_2'] == 'AVELLANEDA']
#padron[padron['departamento'] == 'AVELLANEDA' ]

# iii
# Consideramos los rubros como actividades
rubro['rubro'].value_counts()
# fruticultura (432)

# iv
# Buscamos el clae2 que corresponde al rubro fruticultura
rubro_clae[rubro_clae['rubro'] == 'FRUTICULTURA']
# clae de fruticultura es 1

# Calculamos el salario promedio de fruticultura solo tomando el ultimo de 2022
promedio_2022_1 = sql^"""
SELECT avg(w_median)
FROM salarios
WHERE clae2 = 1 AND fecha LIKE '2022-12-01'
"""
# El salario promedio de 2022 es 195846.372709

#v
#Guardamos salarios agregando la columna anio(año)
salarios = sql^"""
SELECT *, SUBSTRING(fecha, 1, 4) AS anio
FROM salarios
"""

# Calculamos el promedio de salario y el desvio de cada año
promedio_anual_pais = sql^"""
SELECT anio, avg(w_median) AS promedio_anual, stddev(w_median) AS desvio_anual
FROM salarios
GROUP BY anio
ORDER BY anio ASC
"""

# Chequeamos cuantos Na hay en id_provincia en salarios
salarios['id_provincia_indec'].isna().sum()
# como la columna id_provincia_indec tiene ~0.36% valores nulos
# decidimos eliminar esos valores para realizar la siguiente consulta
salarios = salarios.dropna(subset=['id_provincia_indec'])
salarios['id_provincia_indec'].isna().sum()

# Calculamos el promedio anual y su desvío para cada año por provincia
promedio_anual_provincia = sql^"""
SELECT id_provincia_indec, p.provincia_nombre_2, anio, avg(w_median) AS promedio_anual, stddev(w_median) AS desvio_anual
FROM salarios AS s
JOIN provincia AS p
ON s.id_provincia_indec = p.provincia_id
GROUP BY s.anio, s.id_provincia_indec, p.provincia_nombre_2
ORDER BY anio ASC, p.provincia_nombre_2 ASC
"""

# ajustar por la inflacion
# fuente externa: datos de inflación anual

#%%
#### GRAFICOS
# Grafico 1

# Calculamos cuantos operadores tiene cada provincia
# Lo guardamos en un dataFrame
conteo_provincia = pd.DataFrame(padron['provincia_id'].value_counts())
conteo_provincia.reset_index(inplace= True)
conteo_provincia.columns = ['id_provincia', 'Cantidad']


# Ahora unimos conteo_provincia con provincia segun su id
# para obtener el nombre de provincia
conteo_provincia = sql^"""
                        SELECT p.provincia_nombre_2 AS Provincia, c.Cantidad
                        FROM conteo_provincia AS c
                        JOIN provincia AS p
                        ON p.provincia_id = c.id_provincia
                        ORDER BY c.Cantidad DESC
                       """

# Grafico
plt.figure(figsize=(14, 7))
g = sns.barplot(
    x="Cantidad",
    y="Provincia",
    data=conteo_provincia,
    estimator=sum,
    errorbar=None,
    color='#B6D6CC');

for p in g.patches:
    width = p.get_width()
    height = p.get_height()
    x, y = p.get_xy()
    g.annotate(f'{width:.2f}', (x + width, y + height/2), ha='left', va='center')

plt.xlabel('Cantidad de Operadores Certificados')
plt.show()
plt.close()


#Grafico 2

# Calculamos cuantos producto tiene cada operador
conteo_productos = pd.DataFrame(productos['id_registro'].value_counts())
conteo_productos.reset_index(inplace=True)
conteo_productos.columns = ['id_registro', 'Cantidad_productos']

# Unimos conteo_productos con padron segun id_registro
# para saber a que provincia pertenece cada operador
conteo_productos = sql^"""
                        SELECT p.provincia_id, c.Cantidad_productos
                        FROM conteo_productos AS c
                        JOIN padron AS p
                        ON p.id_registro = c.id_registro
                       """

# Usamos el id de cada provincia para determinar su nombre
conteo_productos = sql^"""
                        SELECT p.provincia_nombre_2 AS Provincia, c.Cantidad_productos
                        FROM conteo_productos AS c
                        JOIN provincia AS p
                        ON p.provincia_id = c.provincia_id
                       """

# Calcular la media de la cantidad de productos por provincia
media_por_provincia = conteo_productos.groupby('Provincia')['Cantidad_productos'].median().sort_values(ascending=False).index

# Boxplot
plt.figure(figsize=(10, 7))
g = sns.boxplot(y='Provincia', x='Cantidad_productos', data=conteo_productos,
                 showfliers=False, orient='h', order=media_por_provincia)

# Agregar puntos individuales
g = sns.stripplot(y='Provincia', x='Cantidad_productos',
                   data=conteo_productos, color="grey", jitter=0.2, size=2,
                   orient='h', alpha=0.6, order=media_por_provincia)

plt.title("Boxplot de cantidad de productos por operador por provincia", loc="left")
g.set(xlabel='Cantidad de Productos', ylabel='Provincia')

plt.show()
plt.close()

# Grafico 3

# calculo el promedio de sueldos por clae y provincia
sueldo_provincia_por_clase=sql^ """
SELECT id_provincia_indec, clae2, avg(w_median) AS promedio
FROM salarios
WHERE anio LIKE '2022'
GROUP BY id_provincia_indec, clae2
"""

# necesito la cantidad de operadores por provincia por clae
# al dataframe rubro le agrego su correspondiente clae
df_rubro_clae=sql^"""
SELECT DISTINCT r.id_registro,r.rubro,c.clae2
FROM rubro AS r
JOIN rubro_clae AS c
ON r.rubro = c.rubro
"""

# cuento la cantidad de operadores por provincia por clae
cant_op_provincia_por_clase=sql^"""
SELECT p.provincia_id,r.clae2,count(*) AS cantidad
FROM padron AS p
LEFT JOIN df_rubro_clae AS r
ON p.id_registro = r.id_registro
GROUP BY p.provincia_id,r.clae2
"""

# junto todo en un solo df
grafico3_provincia_id=sql^"""
SELECT DISTINCT *
FROM cant_op_provincia_por_clase AS c
LEFT OUTER JOIN sueldo_provincia_por_clase AS s
ON c.provincia_id = s.id_provincia_indec AND s.clae2 = c.clae2
"""

# agrego los nombres de provincia
grafico3=sql^ """
SELECT DISTINCT g.clae2, g.cantidad, g.promedio, p.provincia_nombre_2
FROM grafico3_provincia_id AS g
LEFT OUTER JOIN provincia as p
ON p.provincia_id = g.provincia_id
"""

# Agrego las descripciones de las clae
grafico3=sql^ """
SELECT DISTINCT g.clae2, c.clae2_desc, g.cantidad, g.promedio, g.provincia_nombre_2
FROM grafico3 AS g
JOIN clases as c
ON g.clae2 = c.clae2
"""

# Scatterplot con colores segun provincia, forma segun actividades
g = sns.scatterplot(data = grafico3 , x = 'cantidad' , y = 'promedio' ,hue = 'provincia_nombre_2',legend=False,style='clae2',)
g.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
plt.xlabel('Cantidad de Operadores')
plt.ylabel('Sueldo Promedio')
plt.grid(True)
plt.show()
plt.close()




# Version actividades en colores
plt.figure(figsize=(10, 7))
g = sns.scatterplot(data = grafico3 , x = 'cantidad' , y = 'promedio' ,hue='clae2_desc',legend=True)
g.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
plt.xlabel('Cantidad de Operadores')
plt.ylabel('Sueldo Promedio')
plt.legend(title='Clae2')
plt.grid(True)
plt.show()
plt.close()

#Grafico 4

# Guardamos los salarios de 2022 con su correspondiente provincia
grafico4 = sql^ """
SELECT *
FROM salarios AS s
JOIN provincia AS p
ON s.id_provincia_indec = p.provincia_id
WHERE s.anio LIKE '2022'
"""

# Como los numeros son muy grandes y dispersos calculamos el log10()
grafico4['log'] = np.log10(grafico4['w_median'])
# Ordenamos las provincias de mayor a menor segun la mediana
my_order = grafico4.groupby(by=["provincia_nombre_2"])["w_median"].median().sort_values(ascending=False).index

#plt.figure(figsize=(35, 15))
sns.violinplot(data = grafico4, x = "log", y="provincia_nombre_2", order = my_order)
plt.xlabel('Log10 (Ingreso Promedio)')
plt.ylabel('Provincia')
#plt.savefig('mi_grafico4.png')
plt.show()
plt.close()

#Grafico 5

# Seleccionamos las 2 provincias con mayor mediana de salario y las 2 con menor
grafico5 = sql^"""
SELECT *
FROM grafico3
WHERE provincia_nombre_2 LIKE 'CIUDAD AUTONOMA DE BUENOS AIRES' OR provincia_nombre_2 LIKE 'TIERRA DEL FUEGO'
OR provincia_nombre_2 LIKE 'CHACO' OR provincia_nombre_2 LIKE 'SANTIAGO DEL ESTERO'
"""

# Grafico
sns.set_theme(style="whitegrid")
g = sns.catplot(
    data=grafico5, kind="bar",
    y="provincia_nombre_2", x="cantidad", hue="clae2_desc", palette="dark", alpha=.6, height=6,legend=False
)
g.despine(left=True)
g.set_axis_labels("Cantidad de operadores", "Provincias")
plt.xticks(ticks=[0,3,6,9], labels=['0','3','6','9'])


# Grafico Anexo 2

# Cantidad de operadores por departamento
# Calculo el promedio de sueldos por clae y provincia y depto
sueldo_depto_por_clase=sql^ """
SELECT id_provincia_indec,codigo_departamento_indec, clae2, avg(w_median) AS promedio
FROM salarios
WHERE anio LIKE '2022'
GROUP BY id_provincia_indec,codigo_departamento_indec, clae2
"""

# Cuento la cantidad de operadores por deptro por clae
cant_op_departamento_por_clase=sql^"""
SELECT p.provincia_id,p.departamento_id_3,r.clae2,count(*) AS cantidad
FROM padron AS p
LEFT JOIN df_rubro_clae AS r
ON p.id_registro = r.id_registro
GROUP BY p.provincia_id,p.departamento_id_3,r.clae2
"""

# Junto todo en un solo df
grafico3_depto_id=sql^"""
SELECT DISTINCT *
FROM cant_op_departamento_por_clase AS c
LEFT OUTER JOIN sueldo_depto_por_clase AS s
ON c.provincia_id = s.id_provincia_indec AND s.clae2 = c.clae2 AND c.departamento_id_3 = s.codigo_departamento_indec
"""

# Agrego los nombres de provincia
grafico3b=sql^ """
SELECT DISTINCT g.clae2, g.cantidad, g.promedio, p.provincia_nombre_2
FROM grafico3_depto_id AS g
LEFT OUTER JOIN provincia as p
ON p.provincia_id = g.provincia_id
"""

# Agrego las descripciones de las clae
grafico3b=sql^ """
SELECT DISTINCT g.clae2, c.clae2_desc, g.cantidad, g.promedio, g.provincia_nombre_2
FROM grafico3b AS g
JOIN clases as c
ON g.clae2 = c.clae2
"""

# Grafico
plt.figure(figsize=(10, 7))
g = sns.scatterplot(data = grafico3b , x = 'cantidad' , y = 'promedio' ,hue = 'clae2_desc')
g.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
plt.xlabel('Cantidad de Operadores por departamento')
plt.ylabel('Sueldo Promedio')
plt.grid(True)
plt.show()
plt.close()

#%%
# 3FN
#Esto se hizo al final para no modificar el código de más arriba
#Lo importante es que estas tablas quedaron respetando la 3FN
Operadores_Organicos = padron.rename(columns={'departamento_id_3': 'departamento_id'})
eliminar_columnas = ['provincia_id', 'departamento', 'categoria_id', 'localidad']
Operadores_Organicos = Operadores_Organicos.drop(eliminar_columnas, axis=1)

provincia = provincia.rename(columns={'provincia_nombre_2': 'provincia_nombre'})

Salario_del_sector_privado = salarios.drop(columns=['anio'])
eliminar_columna = ['id_provincia_indec']
Salario_del_sector_privado = Salario_del_sector_privado.drop(eliminar_columna, axis=1)

localidades = localidades.rename(columns={'nombre_2': 'nombre'})
eliminar_columnas = ['departamento_id', 'provincia_id']
localidades = localidades.drop(eliminar_columnas, axis=1)

municipio = municipio.rename(columns={'municipio_nombre_2': 'municipio_nombre'})
municipio = municipio.dropna(subset=['departamento_id'])
