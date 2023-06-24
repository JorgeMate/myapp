import pandas as pd
#from io import StringIO
import matplotlib.pyplot as plt

df_orig = pd.read_csv("dades.csv", header=0, sep=';')

print(df_orig.columns)

df = df_orig.loc[:, ['Fecha', 'Estación', 'Temperatura']]

# Convertir la columna 'Fecha' a tipo datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Ordenados...
df = df.sort_values('Fecha')


# Mostrar las primeras filas del DataFrame
print(df.head())

# Contar el número de valores faltantes en la columna 'Temperatura'
num_valores_faltantes = df['Temperatura'].isna().sum()

# Mostrar el número de valores faltantes
print("Número de valores faltantes en la columna 'Temperatura':", num_valores_faltantes)

df.dropna(inplace=True)



# Agrupar por 'Fecha' y 'Estación' y obtener la media de 'Temperatura' en cada grupo
df = df.groupby(['Fecha', 'Estación'])['Temperatura'].max().reset_index()




año = 2021
df_año = df.loc[df['Fecha'].dt.year == año]
df_mes = df_año.loc[df['Fecha'].dt.month == 1]

# Obtener los valores únicos de la columna 'Estación'
valores_estacion = df['Estación'].unique()

# Mostrar los valores únicos de la columna 'Estación'
print(valores_estacion)

station_name = "Valencia Centro"
df_estacion = df_mes.loc[df_mes['Estación'] == station_name]

print(df_estacion)

#print(df_estacion)

# Crear el gráfico
plt.plot(df_estacion['Fecha'], df_estacion['Temperatura'])

# Establecer etiquetas y título
plt.xlabel('Fecha')
plt.ylabel('Temperatura')
plt.title('Serie Temporal de Temperaturas')

# Rotar etiquetas del eje x para una mejor visibilidad
plt.xticks(rotation=45)

# # Mostrar el gráfico
plt.show()

