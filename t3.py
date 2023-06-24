import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

df_orig = pd.read_csv("dades.csv", header=0, sep=';', parse_dates=True)

#print(df_orig.columns)
#print(df_orig)

df = df_orig.loc[:, ['Fecha', 'Temperatura']]

# Convertir la columna 'Fecha' a tipo datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Extraer el año y el mes de la columna 'Fecha'
df['Month'] = df['Fecha'].dt.month
df['Year'] = df['Fecha'].dt.year

# Ordenados...
#df = df.sort_values('Fecha')

#print(df)

# Contar el número de valores faltantes en la columna 'Temperatura'
#num_valores_faltantes = df['Temperatura'].isna().sum()

# Mostrar el número de valores faltantes
#print("Número de valores faltantes en la columna 'Temperatura':", num_valores_faltantes)

df.dropna(inplace=True)

# Contar el número de valores faltantes en la columna 'Temperatura'
#num_valores_faltantes = df['Temperatura'].isna().sum()
# Mostrar el número de valores faltantes
#print("Número de valores faltantes en la columna 'Temperatura':", num_valores_faltantes)

#print(df)

if False:

    # Plotting histogram -------------------------------------------
    plt.hist(df['Temperatura'], bins=20, edgecolor='black')

    # Adding labels and title
    plt.xlabel('Temperature')
    plt.ylabel('Frequency')
    plt.title('Temperature Histogram')

    # Display the histogram
    plt.show()


    # Extract the year from the 'Fecha' column
    df['Year'] = df['Fecha'].dt.year

    # Create a box and whisker plot for each year
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Year', y='Temperatura', data=df)
    plt.xlabel('Year')
    plt.ylabel('Temperature')
    plt.title('Temperature Distribution by Year')
    plt.xticks(rotation=45)

    # Display the plot
    plt.show()





# Calculate the monthly average temperature
monthly_avg_temperatures = df.groupby(['Year', 'Month'])['Temperatura'].mean()

# Convert the result to a DataFrame
monthly_avg_temperatures = monthly_avg_temperatures.reset_index()

# Create a new column 'NumericDate' representing the date as numeric values
monthly_avg_temperatures['NumericDate'] = monthly_avg_temperatures['Year'] + monthly_avg_temperatures['Month'] / 12

# Plot the time series
#plt.figure(figsize=(10, 6))
plt.plot(monthly_avg_temperatures['NumericDate'], monthly_avg_temperatures['Temperatura'])
sns.regplot(x='NumericDate', y='Temperatura', data=monthly_avg_temperatures, scatter=False, color='red', label='Regression Line')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Average Temperature')
plt.title('Monthly Average Temperature with Regression Line')
plt.xticks(rotation=45)

# Add a legend
plt.legend()

# Display the plot
plt.show()