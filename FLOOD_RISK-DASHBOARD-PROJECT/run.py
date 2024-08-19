import streamlit as st
import numpy as np
from streamlit_option_menu import option_menu
import properties, model_develop, flood_risk_visuals, flood_risk_overview
st.set_page_config(
    page_title="Hazard Risk Dashboard", layout="wide", 
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
                menu_title='Hazard Risk Dashboard',
                options=['Hazard Risk Overview', 'Data Sources','Model Estimation','Hazard Risk Visualization'],
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
    
    multi_app.add_app("Hazard Risk Overview", flood_risk_overview)
    multi_app.add_app("Model Estimation", model_develop)
    multi_app.add_app("Data Sources", properties)
    multi_app.add_app("Hazard Risk Visualization", flood_risk_visuals)
    
    multi_app.run()


