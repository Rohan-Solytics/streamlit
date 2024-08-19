import streamlit as st
import plotly.express as px
from artifacts import NII_3Y_data

def create_bar_chart(selected_scenarios):
    filtered_data = NII_3Y_data[NII_3Y_data["Scenario"].isin(selected_scenarios)]
    
    custom_colour = ["#272D55", "#AECDFC", "#84AFEF", "#EE883D", "#F7C9A8", '#9396AA', "#F7C9A8", "#EE883D", "#84AFEF", "#AECDFC", "#272D55",] 
    fig = px.bar(filtered_data.sort_values(by="Delta_NII", ascending=False), 
                 x="Scenario", y="Delta_NII", 
                 title="Three Year Delta NII Plot", text_auto=False,
                 color="Scenario", color_discrete_sequence=custom_colour, 
                 labels={"Scenario": "Scenario", "Delta_NII": "Delta NII in %"})
    
    fig.update_layout(xaxis=dict(tickangle=45, tickfont=dict(color='black'),
                                title=dict(font=dict(color='black'))),
                      yaxis=dict(tickfont=dict(color='black'),
                                 title=dict(font=dict(color='black'))),
                      height=400, width=850, title_x=0.25, title_font_size=20,
                      legend_title=dict(font=dict(color='black')),
                      plot_bgcolor='#f4f4f4', paper_bgcolor='#f4f4f4')
    return fig
    return fig

def app():
    # Select scenarios
    all_scenarios = NII_3Y_data["Scenario"].unique()

    with st.expander('Select Scenarios'):
        # Toggle state for Select/Deselect All button
        toggle_state = st.session_state.get("toggle_state_nii_3y", False)
        # Initialize selected_scenarios outside of the if condition
        selected_scenarios = st.session_state.get("selected_scenarios_nii_3y", all_scenarios)

        select_deselect_all_button = st.button("Select/Deselect All")

        if select_deselect_all_button:
            selected_scenarios = all_scenarios if not toggle_state else []
            st.session_state.toggle_state_nii_3y = not toggle_state

        selected_scenarios = st.multiselect(
            "Select Scenario:",
            options=all_scenarios,
            format_func=lambda x: x,
            default=selected_scenarios
        )

    # Display bar chart
    fig_bar = create_bar_chart(selected_scenarios)
    st.plotly_chart(fig_bar)

if __name__ == "__main__":
    app()
