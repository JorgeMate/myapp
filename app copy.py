from shiny import ui, render, App


import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns

df_orig = pd.read_csv("dades.csv", header=0, sep=';', parse_dates=True)
df = df_orig.loc[:, ['Fecha', 'Temperatura', 'NO', 'NO2', 'NOx', 'SO2', 'O3', 'CO']]

df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Month'] = df['Fecha'].dt.month
df['Year'] = df['Fecha'].dt.year

df.dropna(inplace=True)

monthly_avg_temperatures = df.groupby(['Year', 'Month']).mean().reset_index()
monthly_avg_temperatures['NumericDate'] = monthly_avg_temperatures['Year'] + monthly_avg_temperatures['Month'] / 12





app_ui = ui.page_fluid(
    
    
      ui.navset_tab(
        
        ui.nav("Abstract", 
            ui.h5(' '),
            ui.h2("EDM Project, UPV"),
            ui.h5("Title: Air quality in Valencia based on registered data."),
            ui.h5("Author: Jorge Maté Martínez, June 2023"),
            ui.markdown("""
                This app is based on data extracted from [València Open Data][0], and holds hourly quality data 
                registered from 11 surveillance network stations since 2016. 
                
                [0]: https://valencia.opendatasoft.com/explore/dataset/dades-horaris-qualitat-de-laire-desde-2016/information/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6ImRhZGVzLWhvcmFyaXMtcXVhbGl0YXQtZGUtbGFpcmUtZGVzZGUtMjAxNiIsIm9wdGlvbnMiOnt9fSwiY2hhcnRzIjpbeyJhbGlnbk1vbnRoIjp0cnVlLCJ0eXBlIjoibGluZSIsImZ1bmMiOiJBVkciLCJ5QXhpcyI6ImRpYV9kZWxfbWVzIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiIzY2YzJhNSJ9XSwieEF4aXMiOiJob3JhIiwibWF4cG9pbnRzIjoiIiwidGltZXNjYWxlIjoieWVhciIsInNvcnQiOiIifV0sImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9
            """),
            ui.markdown("""
                Data Source: Red Valenciana de Vigilancia y Control 
                de la Contaminación Atmosférica.
            """),
        ),
        
         ui.nav("Display and Explain", 
            ui.layout_sidebar(
                
                ui.panel_sidebar(
                    
                    ui.input_slider("x3", "Rango de Años", value=(2016, 2022), min=2016, max=2022),
                   
                    ui.input_checkbox_group("variables", label="Variables a mostrar", choices=["Temperatura", "Mostrar regresor"], selected=["Temperatura"]),
                    ui.input_checkbox_group("variables2", label="Óxidos Nitrosos", choices=["NO", "NO2", "NOx"], selected=[]),
                    ui.input_checkbox_group("variables3", label="Otros Contaminantes", choices=["SO2", "O3", "CO"], selected=[]),
                   
                                 
                ),
                ui.panel_main(
                    
                    
                     ui.output_plot("plot"),
                    
                    
                     ui.output_ui("my_cool_text"),
                     ui.h5(' '),
                     ui.output_ui("Temperatura"),
                     ui.h5(' '),
                     ui.output_ui("Oxidos_Nitrosos"),
                ),
            ),
        ),
        
        ui.nav("Raw Data", 
            ui.output_table("datos_contaminacion"),
            
         
            
        ),
    
      )
    
   
)










def server(input, output, session):
    @output
    @render.ui
    def my_cool_text():
        selected_variables = input.variables.get()
        selected_variables2 = input.variables2.get()
        selected_variables3 = input.variables3.get()
        if selected_variables or selected_variables2 or selected_variables3:
            
            text = ui.strong("Variables seleccionadas:")
        
                   
            return text
        else:
            return "No hay variables seleccionadas"
        


    @output
    @render.ui
    def Temperatura():
        selected_variables = input.variables.get()
        #selected_variables2 = input.variables2.get()
        #selected_variables3 = input.variables3.get()
        #if selected_variables or selected_variables2 or selected_variables3:
            
        text = ""
        
        if selected_variables:
            for variable in selected_variables:
                if variable == "Temperatura":
                    text += """
            Temperatura. El gráfico muestra la varición interanual de la temperatura 
            media en Valencia segmentada por meses. Los valores aparecen "suavizados" porque
            se promedian temperaturas diurnas y nocturnas. Se observa una tendencia general creciente,
            especialmente al mostrar la regresión generada por el modelo. Es una serie temporal
            con estacionalidad, por lo que se podría predecir con un modelo ARIMA. Se observan
            tanto los picos de temperatura media mensual en verano como los valles en invierno.
            Los inviernos parecen irse haciendo menos fríos, y los veranos más cálidos.
        """

        return text
    #else:
    #    return ""
        
    @output
    @render.ui
    def Oxidos_Nitrosos():
        selected_variables2 = input.variables2.get()
        
        text = ""
        
        if selected_variables2:
           
            text += """
            Los óxidos de nitrógeno (NOx), que incluyen al óxido de nitrógeno (NO) y al dióxido de nitrógeno (NO2), se miden comúnmente en partes por millón (ppm) en el aire que respiramos.
            Son gases irritantes que pueden causar problemas respiratorios, inflamación pulmonar, reducción de la función pulmonar y contribuir a la formación de smog y lluvia ácida.
            Los óxidos de nitrógeno también contribuyen a la formación de partículas finas y ozono troposférico, ambos de los cuales están asociados con efectos adversos para la salud.
        """
        
        
            text += """
            Sus mediciones son utilizadas para evaluar la calidad del aire y determinar si los niveles de contaminantes cumplen con las normas establecidas 
            para la protección de la salud humana y el medio ambiente.
            Puede apreciarse claramente que los niveles de NOx son más altos en invierno, y más bajos en verano.
            """

        return text
        



    @output
    @render.table
    def datos_contaminacion():
        return df.head(10)
    
    @output
    @render.plot
    def plot():
        # Filter the data based on the selected range of years
        selected_years = range(input.x3.get()[0], input.x3.get()[1])

        filtered_data = monthly_avg_temperatures[monthly_avg_temperatures['Year'].isin(selected_years)]
        
        # Plot the filtered data for selected variables
        selected_variables = input.variables.get()
        for variable in selected_variables:
            if variable != "Mostrar regresor":
                plt.plot(filtered_data['NumericDate'], filtered_data[variable], label=variable)
            else:
                sns.regplot(x='NumericDate', y='Temperatura', data=filtered_data, label='Regresión')
            
        selected_variables2 = input.variables2.get()
        for variable2 in selected_variables2:
            plt.plot(filtered_data['NumericDate'], filtered_data[variable2], label=variable2)
        
        selected_variables3 = input.variables3.get()
        for variable3 in selected_variables3:
            plt.plot(filtered_data['NumericDate'], filtered_data[variable3], label=variable3)
        
        
        plt.xlabel('Fecha')
        plt.ylabel('Medición')
        plt.title('Montly evolution in Valencia of the selected air condition variables')
        plt.xticks(rotation=45)
        plt.legend()
        
        fig = plt.gcf()
        return fig
    

app = App(app_ui, server)