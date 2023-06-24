from shiny import App, ui

app_ui = ui.page_fluid(
    # style ----
    ui.navset_tab(
        # elements ----
        ui.nav("a", "tab a content"),
        ui.nav("b", "tab b content"),
    )
)


app = App(app_ui, None)