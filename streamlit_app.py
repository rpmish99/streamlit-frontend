import pandas as pd
import plotly.express as px
import streamlit as st
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# Load data
url = "https://raw.githubusercontent.com/plotly/datasets/master/diabetes-vid.csv"
df = pd.read_csv(url)

# Streamlit app
st.set_page_config(page_title="Diabetes Dashboard", page_icon=":bar_chart:")
st.title("Diabetes Dashboard")

# Create scatter plot using Plotly Express
fig = px.scatter(df, x="BloodPressure", y="BMI", color="Age", title="Blood Pressure vs BMI colored by Age")

# Create Dash app
app = dash.Dash(__name__, prevent_initial_callbacks=True)

# Create dropdown options
outcome_options = [{"label": o, "value": o} for o in df["Outcome"].unique()]

# Create Dash component
app.layout = html.Div(
    [
        html.H1("Diabetes Data"),
        html.Div(
            [
                dcc.Dropdown(
                    id="outcome-filter",
                    options=outcome_options,
                    value=df["Outcome"].unique()[0],
                )
            ]
        ),
        dcc.Graph(id="scatter-plot", figure=fig),
    ]
)

# Callback function to update the scatter plot based on the selected 'Outcome' value
@app.callback(
    Output("scatter-plot", "figure"),
    [Input("outcome-filter", "value")],
)
def update_scatter_plot(selected_outcome):
    filtered_df = df[df["Outcome"] == selected_outcome]
    fig = px.scatter(
        filtered_df, x="BloodPressure", y="BMI", color="Age", title="Blood Pressure vs BMI colored by Age"
    )
    return fig

# Display app
st.plotly_chart(fig)
st.components.v1.html(app.index_string, height=800)

if __name__ == "__main__":
    st.sidebar.header("Filter data")
    app.run_server(debug=True, port=8050)

st.markdown("***")
st.write("Dashboard developed by Amazon Q")
