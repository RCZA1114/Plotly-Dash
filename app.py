from dash import Dash, html, dcc

app = Dash()

app.layout = html.Div(children=[
        html.H1(children='SMACK')
])


if __name__ == '__main__':
            app.run(debug=True)