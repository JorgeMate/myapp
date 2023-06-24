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
            ui.h5("Title: Air quality fast survellance in Valencia based on available registered data."),
            ui.h5("Author: Jorge Maté Martínez, June 2023"),
            ui.h5(' '),
            ui.h5(' '),
            
            ui.markdown("""
                          """),
            
            ui.markdown("""
                This app is based on data extracted from [València Open Data][0], at its original source it is called "Hourly air quality data since 2016". 
                It holds hourly quality data registered from 11 different surveillance network stations since 2016. 
                
                [0]: https://valencia.opendatasoft.com/explore/dataset/dades-horaris-qualitat-de-laire-desde-2016/information/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6ImRhZGVzLWhvcmFyaXMtcXVhbGl0YXQtZGUtbGFpcmUtZGVzZGUtMjAxNiIsIm9wdGlvbnMiOnt9fSwiY2hhcnRzIjpbeyJhbGlnbk1vbnRoIjp0cnVlLCJ0eXBlIjoibGluZSIsImZ1bmMiOiJBVkciLCJ5QXhpcyI6ImRpYV9kZWxfbWVzIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiIzY2YzJhNSJ9XSwieEF4aXMiOiJob3JhIiwibWF4cG9pbnRzIjoiIiwidGltZXNjYWxlIjoieWVhciIsInNvcnQiOiIifV0sImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9
            """),
            ui.markdown("""
                Original Data Source: 
                Red Valenciana de Vigilancia y Control de la Contaminación Atmosférica.
            """),
            
            ui.markdown("""
                This work is a first approach to use interactive tools to handle a data model online, 
                and it is intended to be a fast and easy way to visualize available real data.
            """),
            
            ui.markdown("""
                STACK SELECTION: A trade-off between two needs has arisen: The construction of a complex or useful model, 
                and the need to dedicate time to the learning courve of a new tool able to offer interactivity and fast deployment.
                Exploring the pros and cons of different tools, it has been decided to use the Shiny library for python. As seems
                easier to learn and deploy, and it is based on a well known library for R, it has been chosen for this project.
                Some time has logically been consumed to learn the basics of the library, about funtionality but also about its 
                deployment possibilities and authentication mechanisms.
            """),
            
            ui.markdown("""
                DATA SELECTION: After exploring the propossed datasets, it has been deciden to use an air quality data repository, as it is easy
                to explain and understand. It is also a topic of interest for the society. The contained data is time series like, and seems
                a good candidate for a first approach to the use of interactive tools. There is a data dictionary available (with not so rich 
                metadata available) in the included link. The final aspect of the processed data is shown in the Raw Data samples tab.
            """),
            
            
            ui.markdown("""
                DATA PREPROCESSING: In order to show a global picture of the city air conditions, the data has been undistinguishably selected 
                among all the stations, and then grouped (averaged) by month and year, as we are interested in exploring very general patterns.    
            """),
            
            ui.markdown("""
                MISSING VALUES: All records counting with any number of NA values have been previously removed from the dataset.   
            """),
            
            ui.markdown("""
                DESIGN AND INTERACTIVITY: The effort has been focussed in creating some real interactive controls to manipulate the displayed
                information, that itself also intends to be realistic and useful. Some design decorations, using tabs and another available html resources
                have also been experimented.
                
            """),
            
            ui.markdown("""
                MODEL GOAL: To offer a fast but realistic view of the air quality in Valencia showing the evolution of the main 
                contributor contamination variables. As changing temperatures are also a main factor for air conditions (and also a tred thopic), 
                The temperature has been included in the model.
                
            """),
            
            ui.markdown("""
                FUTURE EXTENSIONS: A prioritary goal would be to get the data directly from the available data source via its API. It would give the
                model a nice chance to always display updated data for public availability. Another interesting extension would be to include a prediction model, based on the
                available data, to predict the future evolution of the air quality in Valencia beyond the simple regression line shown in the actual model.
                
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
                     ui.h5(' '),
                     ui.output_ui("Otros_Contaminantes"),
                ),
            ),
        ),
        
        ui.nav("Raw Data samples", 
            ui.output_table("datos_contaminacion"),   
        ),
    
    )
)


#############################################################################3333

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
            Temperatura. El gráfico muestra la variación interanual de la temperatura 
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
            Puede apreciarse claramente que sus niveles de son más altos en invierno, y más bajos en verano.
            """

        return text
        
    @output
    @render.ui
    def Otros_Contaminantes():
        selected_variables3 = input.variables3.get()
        
        text = ""
        
        if selected_variables3:
           
            text += """
            El dióxido de azufre (SO2) es un gas incoloro con un olor acre irritante. Es un subproducto de la combustión de combustibles fósiles que contienen azufre, 
            como el carbón y el petróleo. El dióxido de azufre se emite en el aire por las centrales eléctricas y las plantas industriales que queman carbón o petróleo. 
            Algunas industrias, como la fabricación de papel, la fabricación de metales y la fabricación de alimentos, liberan dióxido de azufre.
            También se miden comúnmente en partes por millón (ppm)
            """
        
        
            text += """
            El ozono (O3) es un gas incoloro que se encuentra naturalmente en la atmósfera superior de la Tierra. 
            La capa de ozono en la atmósfera superior protege la Tierra de la radiación ultravioleta del sol. 
            Sin embargo, el ozono en la atmósfera inferior es un contaminante que puede causar problemas de salud.
            """
            
            text += """
            El monóxido de carbono (CO) es un gas incoloro e inodoro que se produce cuando se quema combustible. 
            Los motores de los vehículos y los calentadores de espacio, como los utilizados en los campamentos, producen monóxido de carbono.
            """
            
            text += """
            Los niveles de SO2, O3 y CO son más altos en verano, y más bajos en invierno.
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