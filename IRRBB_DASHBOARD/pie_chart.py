# import streamlit as st
# import plotly.express as px
# from artifacts import line_items_data

# def create_pie_chart(selected_line_items):
#     filtered_data = line_items_data[line_items_data["Line Items"].isin(selected_line_items)]
    
#     # Custom blue color sequence
#     custom_colour = ["#272D55", "#AECDFC", "#84AFEF", "#EE883D", "#F7C9A8", '#9396AA']

#     fig = px.pie(filtered_data, names="Line Items", values="Total Exposure", 
#                  title="Total Exposure by Line Items", 
#                  color_discrete_sequence=custom_colour,
#                  )
#     fig.update_traces(textposition='inside', textinfo='percent')
#     fig.update_layout(height=500, width=850, title_x=0.25, title_font_size=20, plot_bgcolor='#f4f4f4',paper_bgcolor='#f4f4f4')
#     return fig

# def app():
#     # Initialize selected_line_items with all_line_items initially
#     all_line_items = line_items_data["Line Items"].tolist()
#     selected_line_items = all_line_items

#     with st.expander("Select Line Items"):
#         # Use a separate variable to track the toggle state
#         toggle_state = st.session_state.get("toggle_state", True)
#         select_deselect_all_button = st.button("Select/Deselect All")

#         if select_deselect_all_button:
#             # Toggle between selecting all and deselecting all
#             selected_line_items = all_line_items if not toggle_state else []
#             # Update toggle state
#             st.session_state.toggle_state = not toggle_state

#         # Display list items dynamically
#         selected_line_items = st.multiselect(
#             "Line Items:", 
#             options=all_line_items, 
#             format_func=lambda x: x, 
#             default=selected_line_items,
#         )
#     # Display pie chart below the floating container
#     fig = create_pie_chart(selected_line_items)
#     st.plotly_chart(fig)



##---------------------##

import streamlit as st
import plotly.express as px
from artifacts import line_items_data

def create_bar_chart(selected_line_items):
    filtered_data = line_items_data[line_items_data["Line Items"].isin(selected_line_items)]
    
    # Custom blue color sequence
    custom_colour = ["#272D55", "#AECDFC", "#84AFEF", "#EE883D", "#F7C9A8", '#9396AA']
    
    fig = px.bar(filtered_data.sort_values(by="Total Exposure", ascending=False), 
                 x="Line Items", y="Total Exposure",color="Line Items", color_discrete_sequence=custom_colour, 
                 title="Total Exposure by Line Items",
                 labels={"Line Items": "Line Items", "Total Exposure": "Total Exposure"})
    
    fig.update_layout(xaxis=dict(tickangle=45, tickfont=dict(color='black'),
                                title=dict(font=dict(color='black'))),
                      yaxis=dict(tickfont=dict(color='black'),
                                 title=dict(font=dict(color='black'))),
                      height=500, width=850, title_x=0.25, title_font_size=20,
                      legend_title=dict(font=dict(color='black')),
                      plot_bgcolor='#f4f4f4', paper_bgcolor='#f4f4f4')
    return fig

def create_pie_chart(selected_line_items):
    filtered_data = line_items_data[line_items_data["Line Items"].isin(selected_line_items)]
    
    # Custom blue color sequence
    custom_colour = ["#272D55", "#AECDFC", "#84AFEF", "#EE883D", "#F7C9A8", '#9396AA']

    fig = px.pie(filtered_data, names="Line Items", values="Total Exposure", 
                 title="Total Exposure by Line Items", 
                 color_discrete_sequence=custom_colour,
                 )
    fig.update_traces(textposition='inside', textinfo='percent')
    fig.update_layout(height=500, width=850, title_x=0.25, title_font_size=20, plot_bgcolor='#f4f4f4',paper_bgcolor='#f4f4f4')
    return fig

def app():
    # Initialize selected_line_items with all_line_items initially
    all_line_items = line_items_data["Line Items"].tolist()
    selected_line_items = all_line_items

    with st.expander("Select Line Items"):
        # Use a separate variable to track the toggle state
        toggle_state = st.session_state.get("toggle_state", True)
        select_deselect_all_button = st.button("Select/Deselect All")

        if select_deselect_all_button:
            # Toggle between selecting all and deselecting all
            selected_line_items = all_line_items if not toggle_state else []
            # Update toggle state
            st.session_state.toggle_state = not toggle_state

        # Display list items dynamically
        selected_line_items = st.multiselect(
            "Line Items:", 
            options=all_line_items, 
            format_func=lambda x: x, 
            default=selected_line_items,
        )

    # Tabs for selecting chart type
    tab1, tab2 = st.tabs(["Bar Chart", "Pie Chart"])

    with tab1:
        # Display bar chart
        fig_bar = create_bar_chart(selected_line_items)
        st.plotly_chart(fig_bar)
    with tab2:
        # Display pie chart
            fig_pie = create_pie_chart(selected_line_items)
            st.plotly_chart(fig_pie)