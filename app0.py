from shiny import App, render, ui

import pandas as pd

df = pd.read_csv('dades.csv')

print(df.describe())

app_ui = ui.page_fluid(
    
    ui.h2("EDM Project, UPV 2023"),
    ui.h5("Title: Air quality in Valencia. Historical análisis and prediction."),
    ui.h5("Author: Jorge Maté Martínez"),
    
    ui.markdown("""
        This app is based on data extracted from [València Open Data][0], and holds hourly quality data 
        registered from 11 surveillance network stations since 2016. 
        
        [0]: https://valencia.opendatasoft.com/explore/dataset/dades-horaris-qualitat-de-laire-desde-2016/information/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6ImRhZGVzLWhvcmFyaXMtcXVhbGl0YXQtZGUtbGFpcmUtZGVzZGUtMjAxNiIsIm9wdGlvbnMiOnt9fSwiY2hhcnRzIjpbeyJhbGlnbk1vbnRoIjp0cnVlLCJ0eXBlIjoibGluZSIsImZ1bmMiOiJBVkciLCJ5QXhpcyI6ImRpYV9kZWxfbWVzIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiIzY2YzJhNSJ9XSwieEF4aXMiOiJob3JhIiwibWF4cG9pbnRzIjoiIiwidGltZXNjYWxlIjoieWVhciIsInNvcnQiOiIifV0sImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9
    """),
    
        ui.markdown("""
        
        Source: Red Valenciana de Vigilancia y Control 
        de la Contaminación Atmosférica.

        
    """),
    
    
    ui.layout_sidebar(

        ui.panel_sidebar(

    
            ui.input_slider("n", "N", 0, 100, 20),
            ui.output_text_verbatim("txt"),
            
        ),
        
        ui.panel_main(
            
           
        ),
        
    )
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"n*2 is {input.n() * 2}"


app = App(app_ui, server)
