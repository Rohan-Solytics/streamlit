import streamlit as st
import plotly.express as px
from artifacts import Delta_EVE_data

def create_bar_chart(selected_scenarios):
    filtered_data = Delta_EVE_data[Delta_EVE_data["Scenario"].isin(selected_scenarios)]
    
    custom_colour = ["#272D55", "#AECDFC", "#84AFEF", "#9396AA", "#EE883D","#AECDFC", "#272D55"]
    fig = px.bar(filtered_data, x="Scenario", y="Delta_EVE", 
                 title="Delta EVE Plot", color='Scenario',
                 color_discrete_sequence=custom_colour, 
                 labels={"Scenario": "Scenario", "Delta_EVE": "Delta EVE in %"})
    
    fig.update_layout(xaxis=dict(tickangle=45, tickfont=dict(color='black'),
                                title=dict(font=dict(color='black'))),
                      yaxis=dict(tickfont=dict(color='black'),
                                 title=dict(font=dict(color='black'))),
                      height=400, width=850, title_x=0.25, title_font_size=20,
                      legend_title=dict(font=dict(color='black')),
                      plot_bgcolor='#f4f4f4', paper_bgcolor='#f4f4f4')
    return fig

def app():
    # Select scenarios
    all_scenarios = Delta_EVE_data["Scenario"].tolist()

    with st.expander("Select Scenarios"):
        # Toggle state for Select/Deselect All button
        toggle_state = st.session_state.get("toggle_state", True)
        # Initialize selected_scenarios outside of the if condition
        selected_scenarios = st.session_state.get("selected_scenarios", all_scenarios)

        select_deselect_all_button = st.button("Select/Deselect All")

        if select_deselect_all_button:
            selected_scenarios = all_scenarios if not toggle_state else []
            st.session_state.toggle_state = not toggle_state

        selected_scenarios = st.multiselect(
            "Select Scenario:",
            options=all_scenarios,
            format_func=lambda x: x,
            default=selected_scenarios
        )

    # Display bar chart
    fig_bar = create_bar_chart(selected_scenarios)
    st.plotly_chart(fig_bar)