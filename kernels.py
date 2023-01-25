import numpy as np
from numpy import exp, log, log1p, abs
import plotly.graph_objects as go
from ast import literal_eval

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots


contours_z = dict(
    dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True),
)

number_kwargs = dict(type="number", value=0, style={'marginRight': '10px'})
app = Dash(__name__)
app.layout = html.Div([
    html.P(["f(x, z)=", dcc.Input(id='func', type='text',
                                  value='exp(x) / 100 - x ** 2 * z ** 2 + log1p(abs(x))',
                                  debounce=True, style={'width': '1000px'})]),
    dcc.Graph(id="graph"),
    html.P('degree'),
    dcc.Slider(id='degree', min=1, max=20, value=2, step=1),
    html.P('lambda'),
    dcc.Slider(id='lambda', min=0, max=3, value=1, step=0.1),
])


@app.callback(
    Output("graph", "figure"),
    Input("func", "value"),
    Input("degree", "value"),
    Input("lambda", "value"),

)
def plot_sin(func, degree, lambda_):
    size = 50
    x, z = np.mgrid[-1:1:2 / size, -1:1:2 / size]
    f = eval('lambda x, z: ' + func)
    Y = f(x, z)

    X = np.vstack((x.flatten(), z.flatten())).T
    y = Y.flatten()

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.1)
    K_train = (1 + X_train @ X_train.T) ** degree

    model = y_train @ np.linalg.inv(K_train + lambda_ * np.eye(*K_train.shape))
    K = (1 + X_train @ X.T) ** degree
    y_pred = model @ K

    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{'type': 'surface'}, {'type': 'surface'}, {'type': 'xy'}]],
        subplot_titles=("True Surface", f"Predicted Surface, <br>r2: {r2_score(y, y_pred).round(2)}", "Predictions")
    )

    fig.add_trace(go.Surface(z=y_pred.reshape(size, size), x=x, y=z), row=1, col=2)
    fig.update_traces(contours_z=contours_z, showscale=False, row=1, col=2)
    fig.add_trace(go.Surface(z=Y, x=x, y=z), row=1, col=1)
    fig.update_traces(contours_z=contours_z, showscale=False, row=1, col=1)
    fig.update_layout(title='Predicted', autosize=False,
                      width=2400, height=800,
                      margin=dict(l=65, r=50, b=65, t=90))
    fig.add_trace(go.Scatter(x=y, y=y_pred, mode='markers', name='predicted'))
    fig.add_trace(go.Scatter(x=y, y=y, opacity=0.75, name='ideal'))

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
