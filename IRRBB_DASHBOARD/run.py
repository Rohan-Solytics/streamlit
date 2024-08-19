import streamlit as st
import numpy as np
from streamlit_option_menu import option_menu
import pie_chart, delta_eve_ns_plot, delta_eve_plot, delta_nii_1y_plot, delta_nii_3y_plot, eve_summary_report, base_report, nii_summary_report
import requests
from base import file_contents


st.set_page_config(
    page_title="IRRBB Dashboard", layout="wide", 
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
                menu_title='IRRBB Modules',
                options=['Overview', 'Total Exposure', 'Delta EVE Plotting', 'Delta EVE_NS Plotting', 'One Year Delta NII Plot', 'Three Year Delta NII Plot', 'EVE Summary Report', 'NII Summary Report','Base Report'],
                icons=['cast', 'pie-chart', 'triangle', 'triangle', 'calendar', 'calendar', 'book', 'book', 'database'],
                menu_icon=':bank:',
                default_index=0,
                styles={
                    "container": {"padding": "50px", "background-color": 'white', "border-radius": "5px"},
                    "icon": {"color": "#008080", "font-size": "23px"},
                    "nav-link": {"color": "black", "font-size": "15px", "text-align": "left", "margin": "2px", "--hover-color": "#B9DFFE", "font-family": "sans-serif",},
                    "nav-link-selected": {"background-color": "#AFDBF5", "border-radius": "5px"},
                }
            )

        if app == "Overview":
            container = st.container()

            # Centered text in the floating container
            with container:
                st.markdown(
                    """
                    <div style="text-align: center;">
                        <h2>Welcome to IRRBB Dashboard</h2>
                    </div>

                    <div style="text-align: justify;">
                    <p>Interest Rate Risk in the Banking Book (IRRBB) refers to the potential threat posed to a bank's capital and earnings due to fluctuations in interest rates. These fluctuations can impact the bank's balance sheet and its various positions in the banking book. The shape of the interest rate curve, whether steepening, flattening, humped, or inverted, can significantly affect a bank's Net Interest Income (NII), which forms a primary source of earnings.</p>
                    </div>
                    """,

                    unsafe_allow_html=True
                )

                # Display image below the text
                st.image(file_contents,use_column_width=True, caption = "Workflow of Solytics IRRBB Calculator")
        else:
            selected_app = next((a for a in self.apps if a["title"] == app), None)
            if selected_app:
                selected_app["function"].app()


if __name__ == "__main__":
    multi_app = MultiApp()
    
    multi_app.add_app("Total Exposure", pie_chart)
    multi_app.add_app("Delta EVE Plotting", delta_eve_plot)
    multi_app.add_app("Delta EVE_NS Plotting", delta_eve_ns_plot)
    multi_app.add_app("One Year Delta NII Plot", delta_nii_1y_plot)
    multi_app.add_app("Three Year Delta NII Plot", delta_nii_3y_plot)
    multi_app.add_app("EVE Summary Report", eve_summary_report)
    multi_app.add_app("NII Summary Report", nii_summary_report)
    multi_app.add_app("Base Report", base_report)

    multi_app.run()


