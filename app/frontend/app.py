import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask
from flask import redirect, render_template
from dash.dependencies import Input, Output, State
import requests
import logging


server = Flask(__name__)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(server=server, external_stylesheets=external_stylesheets, routes_pathname_prefix='/')


app.title = 'Healthcare App'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[
        html.H1(
            children='Predict Healthcare Cost',
            style={
                'textAlign': 'center'
            }
        ),
        html.H3(
            children='Application to Predict Annual Responsibility for Medicare Patients',
            style={
                'textAlign': 'center'
            }
        ),
        html.Br(),
        html.Br(),
        html.Div([
            html.Div([
                html.Label('Age:'),
                dcc.Input(id='age', style={'width': '50px'}),
                ], className='two columns'),
            html.Div([
                html.Label('Gender:'),
                dcc.Dropdown(
                    id='gender',
                    options=[
                        {'label': 'Male', 'value': '1'},
                        {'label': 'Female', 'value': '2'}
                    ],
                    style={'width': '100px'}
                )], className='two columns'),
            html.Div([
                html.Label('Race:'),
                dcc.Dropdown(
                    id='race',
                    options=[
                        {'label': 'White', 'value': '1'},
                        {'label': 'Black', 'value': '2'},
                        {'label': 'Hispanic', 'value': '5'},
                        {'label': 'Other', 'value': '3'},
                    ],
                    style={'width': '120px'}
                )], className='two columns'),
            html.Div([
                html.Label('State(Abbr.):'),
                dcc.Input(id='state', type='text', style={'width': '50px'})
                ], className='two columns')
        ], className='row', style={
                                    'width': '100%',
                                    'display': 'flex',
                                    'align-items': 'center',
                                    'justify-content': 'center'
                            }
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div(
            html.Div([
                html.Label('Medical Conditions (Select All that Apply):'),
                dcc.Dropdown(
                    id='conditions',
                    options=[
                        {'label': 'Alzheimers', 'value': 'alz'},
                        {'label': 'Heart Failure', 'value': 'hf'},
                        {'label': 'Kidney Disease', 'value': 'kd'},
                        {'label': 'Cancer', 'value': 'cr'},
                        {'label': 'COPD', 'value': 'copd'},
                        {'label': 'Depression', 'value': 'depr'},
                        {'label': 'Diabetes', 'value': 'dia'},
                        {'label': 'Heart Disease', 'value': 'hd'},
                        {'label': 'Osteoporosis', 'value': 'ost'},
                        {'label': 'Arthritis', 'value': 'art'},
                        {'label': 'Stroke', 'value': 'stk'}
                    ],
                    multi=True
                )], style={'width': '30%'}),
            style={
                    'width': '100%',
                    'display': 'flex',
                    'align-items': 'center',
                    'justify-content': 'center'
                }
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div([
            html.Div([
                html.Label(children='Diagnosis Claims Per Year:', style={'width': '70%'}),
                dcc.Input(id='dx', style={'width': '50px'})
            ], className='two columns'),
            html.Div([
                html.Label('Procedures Per Year:', style={'width': '50%'}),
                dcc.Input(id='px', style={'width': '50px'})
            ], className='two columns'),
            html.Div([
                html.Label('Claims Outside of Primary Insurance:', style={'width': '70%'}),
                dcc.Input(id='hcpcs', style={'width': '50px'})
            ], className='two columns')
        ], className='row', style={
                                    'width': '100%',
                                    'display': 'flex',
                                    'align-items': 'center',
                                    'justify-content': 'center'
                            }
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div(
            html.Button('Submit', id='submit-val', style={'width': '25%'}),
            style={
                    'width': '100%',
                    'display': 'flex',
                    'align-items': 'center',
                    'justify-content': 'center'
            }
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H3(id='output', style={'textAlign': 'center'}),
    ], style={'overflow': 'hidden'}),
])


@server.route('/api')
def api_reroute():
    return redirect('/api/')


@server.route('/404')
@server.errorhandler(404)
def page_not_found():
    return render_template('page_not_found.html'), 404


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return app.layout
    else:
        return dcc.Location(pathname='/404', id='404')


@app.callback(
    Output('output', 'children'),
    [Input('submit-val', 'n_clicks')],
    state=[State('age', 'value'),
           State('gender', 'value'),
           State('race', 'value'),
           State('state', 'value'),
           State('conditions', 'value'),
           State('dx', 'value'),
           State('px', 'value'),
           State('hcpcs', 'value')])
def predict(n_clicks, age, gender, race, state, conditions, dx, px, hcpcs):
    if n_clicks is None:
        pass
    else:
        try:
            if age is None:
                raise Exception('Must input age')
            else:
                try:
                    age = int(age)
                except Exception as e:
                    raise Exception('Age must be a number')
            if gender is None:
                raise Exception('Gender must be Male or Female')
            else:
                gender = int(gender)
            if race is None:
                race = 3
            else:
                race = int(race)
            if state is None:
                state = 54
            if conditions is None:
                alzheimers = 2
                heart_failure = 2
                kidney_disease = 2
                cancer = 2
                copd = 2
                depression = 2
                diabetes = 2
                heart_disease = 2
                stroke = 2
                osteoporosis = 2
                arthritis = 2
                stroke = 2
            else:
                if 'alz' in conditions:
                    alzheimers = 1
                else:
                    alzheimers = 2
                if 'hf' in conditions:
                    heart_failure = 1
                else:
                    heart_failure = 2
                if 'kd' in conditions:
                    kidney_disease = 1
                else:
                    kidney_disease = 2
                if 'cr' in conditions:
                    cancer = 1
                else:
                    cancer = 2
                if 'copd' in conditions:
                    copd = 1
                else: 
                    copd = 2
                if 'depr' in conditions:
                    depression = 1
                else:
                    depression = 2
                if 'dia' in conditions:
                    diabetes = 1
                else:
                    diabetes = 2
                if 'hd' in conditions:
                    heart_disease = 1
                else: 
                    heart_disease = 2
                if 'ost' in conditions:
                    osteoporosis = 1
                else:
                    osteoporosis = 2
                if 'art' in conditions:
                    arthritis = 1
                else:
                    arthritis = 2
                if 'stk' in conditions:
                    stroke = 1
                else:
                    stroke = 2
            if dx is None:
                dx = 0
            else:
                dx = int(dx)
            if px is None:
                px = 0
            else:
                px = int(px)
            if hcpcs is None:
                hcpcs = 0
            else:
                hcpcs = int(hcpcs)

            payload = {'age': age, 'gender': gender, 'race': race, 'state': state,
                       'alzheimers': alzheimers, 'heart_failure': heart_failure,
                       'kidney_disease': kidney_disease, 'cancer': cancer,
                       'copd': copd, 'depression': depression, 'diabetes': diabetes,
                       'heart_disease': heart_disease, 'osteoporosis': osteoporosis,
                       'arthritis': arthritis, 'stroke': stroke, 'dx': dx, 'px': px,
                       'hcpcs': hcpcs}
 
            response = requests.post('http://34.102.187.98/api/prediction',
                                     json=payload, verify=True)

            dict_response = dict(response.json())

            if list(dict_response.keys())[0] == 'prediction':
                return 'Predicted Annual Responsibility Cost: ${}'.format(dict_response['prediction'])
            else:
                return dict_response['error']

        except Exception as e:
            logging.error(e)
            return str(e)


if __name__ == '__main__':
    from waitress import serve
    serve(server, host='0.0.0.0', port='80')
