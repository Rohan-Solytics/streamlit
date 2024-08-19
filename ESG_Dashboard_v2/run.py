import streamlit as st
import numpy as np
from streamlit_option_menu import option_menu
import data_display, ifrs_metrics, reporting, emission_overview

st.set_page_config(
    page_title="Emission Dashboard", layout="wide", 
)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title='Emission Dashboard',
                options=['Emission Overview', 'Carbon Footprint', 'IFRS Metrics', 'Sustainability Reporting'],
                icons=['cast', 'file-earmark-arrow-up', 'collection', 'grid', 'graph-up-arrow','receipt'],
                menu_icon=':bank:',
                default_index=0,
                styles={
                    "container": {"padding": "50px", "background-color": 'white', "border-radius": "5px"},
                    "icon": {"color": "#008080", "font-size": "23px"},
                    "nav-link": {"color": "black", "font-size": "15px", "text-align": "left", "margin": "2px", "--hover-color": "#B9DFFE", "font-family": "sans-serif",},
                    "nav-link-selected": {"background-color": "#AFDBF5", "border-radius": "5px"},
                }
            )

        selected_app = next((a for a in self.apps if a["title"] == app), None)
        if selected_app:
            selected_app["function"].app()


if __name__ == "__main__":
    multi_app = MultiApp()
    
    multi_app.add_app("Emission Overview", emission_overview)
    # multi_app.add_app("Import Data", data_import)
    multi_app.add_app("Carbon Footprint", data_display)
    multi_app.add_app("IFRS Metrics", ifrs_metrics)
    # multi_app.add_app("Scenario Analysis", scenario_analysis)
    multi_app.add_app("Sustainability Reporting", reporting)
    
    multi_app.run()


