import streamlit as st
import pandas as pd


def app():
    container = st.container()

    # Centered text in the floating container
    with container:

        st.markdown(
                    """
                    <div style='background-color: #AECDFC; border-radius: 5px; padding: 1px;'>
                        <h1 style='text-align: center; font-size: 28px; color: black;'>Welcome to Hazard Risk Assessment Dashboard</h1>
                    </div>
                    """,
                    unsafe_allow_html=True)
        
        st.markdown(
            """
            <div style="text-align: justify;">
            <p></p>
            <p> Hazard risk assessment dashboard for analysing risk in real-estate properties.
            </p>
            </div>
            """,

            unsafe_allow_html=True
        )
        

        # # Display image below the text
        st.image('image.png',use_column_width=True, caption = "Workflow of Hazard Risk Assesment")
       