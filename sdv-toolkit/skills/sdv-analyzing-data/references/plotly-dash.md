# Plotly Dash Applications

## Minimal Dash App

```python
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

app = Dash(__name__)

df = px.data.gapminder()

app.layout = html.Div([
    html.H1("Dashboard"),
    dcc.Dropdown(df.country.unique(), 'Canada', id='country'),
    dcc.Graph(id='graph')
])

@callback(
    Output('graph', 'figure'),
    Input('country', 'value')
)
def update_graph(country):
    return px.line(df[df.country == country], x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=True)
```

## Key Components

- `dcc.Dropdown`, `dcc.Slider` — Inputs
- `dcc.Graph` — Plotly charts
- `dcc.DataTable` — Interactive tables
- `html.Div`, `html.H1` — Layout

## Deployment

```bash
# requirements.txt
dash
gunicorn

# Procfile
web: gunicorn app:server
```
