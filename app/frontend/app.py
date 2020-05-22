import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask import Flask
from flask import redirect, render_template
from dash.dependencies import Input, Output, State
import requests
from google.cloud import logging as cloudlogging
import logging
import time

log_client = cloudlogging.Client()
log_handler = log_client.get_default_handler()
cloud_logger = logging.getLogger("cloudLogger")
cloud_logger.setLevel(logging.INFO)
cloud_logger.addHandler(log_handler)

server = Flask(__name__)
app = dash.Dash(
    server=server,
    external_stylesheets=[dbc.themes.LUX],
    routes_pathname_prefix="/",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink("API Docs", href="http://34.102.187.98/api/", target="_blank")
        ),
    ],
    brand="Healthcare Predictions",
    brand_href="http://34.102.187.98",
    color="primary",
    dark=True,
)

jumbotron = dbc.Jumbotron(
    [
        dbc.Row(
            [
                dbc.Container(
                    dbc.Col(
                        [
                            html.H1("Healthcare Predictions", className="display-5"),
                            html.P(
                                "An application to predict the "
                                "annual responsibility cost for Medicare/Medicaid patients "
                                "based on medical condition.",
                                className="lead",
                            ),
                            html.Hr(className="my-2"),
                            html.P(
                                "Data taken from the Center for Medicare "
                                "and Medicaid Services."
                            ),
                            html.A(
                                html.P(
                                    dbc.Button("Learn more", color="primary"),
                                    className="lead",
                                ),
                                href="https://www.cms.gov",
                                target="_blank",
                            ),
                        ]
                    ),
                )
            ]
        )
    ],
    fluid=True,
)

form = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Input Information", className="card-title"),
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.FormGroup(
                                            [
                                                dbc.Label("Age:", html_for="age"),
                                                dbc.Input(
                                                    type="integer",
                                                    id="age",
                                                    placeholder="Enter Age",
                                                ),
                                                dbc.FormFeedback(valid=True),
                                                dbc.FormFeedback(
                                                    "Age must be a number", valid=False,
                                                ),
                                            ]
                                        ),
                                        md={"size": 2, "order": 1},
                                    ),
                                    dbc.Col(
                                        dbc.FormGroup(
                                            [
                                                dbc.Label("Gender:", html_for="gender"),
                                                dcc.Dropdown(
                                                    id="gender",
                                                    options=[
                                                        {
                                                            "label": "Male",
                                                            "value": "1",
                                                        },
                                                        {
                                                            "label": "Female",
                                                            "value": "2",
                                                        },
                                                    ],
                                                ),
                                            ]
                                        ),
                                        md={"size": 2, "order": 2, "offset": 1},
                                    ),
                                    dbc.Col(
                                        dbc.FormGroup(
                                            [
                                                dbc.Label("Race:", html_for="race"),
                                                dcc.Dropdown(
                                                    id="race",
                                                    options=[
                                                        {
                                                            "label": "White",
                                                            "value": "1",
                                                        },
                                                        {
                                                            "label": "Black",
                                                            "value": "2",
                                                        },
                                                        {
                                                            "label": "Hispanic",
                                                            "value": "5",
                                                        },
                                                        {
                                                            "label": "Other",
                                                            "value": "3",
                                                        },
                                                    ],
                                                ),
                                            ]
                                        ),
                                        md={"size": 2, "order": 3, "offset": 1},
                                    ),
                                    dbc.Col(
                                        dbc.FormGroup(
                                            [
                                                dbc.Label("State:", html_for="state"),
                                                dbc.Input(
                                                    type="text",
                                                    id="state",
                                                    placeholder="Enter state",
                                                ),
                                                dbc.FormText(
                                                    "State must be abbreviated"
                                                ),
                                                dbc.FormFeedback(valid=True),
                                                dbc.FormFeedback(
                                                    "State must be abbreviated (example: CA)",
                                                    valid=False,
                                                ),
                                            ]
                                        ),
                                        md={"size": 2, "order": 4, "offset": 1},
                                    ),
                                ],
                                align="start",
                                justify="center",
                            ),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            dbc.Row(
                                dbc.Col(
                                    dbc.FormGroup(
                                        [
                                            dbc.Label(
                                                "Medical Conditions (Select All that Apply):",
                                                html_for="conditions",
                                            ),
                                            dcc.Dropdown(
                                                id="conditions",
                                                options=[
                                                    {
                                                        "label": "Alzheimers",
                                                        "value": "alz",
                                                    },
                                                    {
                                                        "label": "Heart Failure",
                                                        "value": "hf",
                                                    },
                                                    {
                                                        "label": "Kidney Disease",
                                                        "value": "kd",
                                                    },
                                                    {"label": "Cancer", "value": "cr"},
                                                    {"label": "COPD", "value": "copd"},
                                                    {
                                                        "label": "Depression",
                                                        "value": "depr",
                                                    },
                                                    {
                                                        "label": "Diabetes",
                                                        "value": "dia",
                                                    },
                                                    {
                                                        "label": "Heart Disease",
                                                        "value": "hd",
                                                    },
                                                    {
                                                        "label": "Osteoporosis",
                                                        "value": "ost",
                                                    },
                                                    {
                                                        "label": "Arthritis",
                                                        "value": "art",
                                                    },
                                                    {"label": "Stroke", "value": "stk"},
                                                ],
                                                multi=True,
                                            ),
                                        ],
                                    ),
                                    md={"size": 5},
                                ),
                                align="center",
                                justify="center",
                            ),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.FormGroup(
                                            [
                                                dbc.Label(
                                                    "Diagnosis Claims Per Year:",
                                                    html_for="dx",
                                                ),
                                                dbc.Input(
                                                    type="integer",
                                                    id="dx",
                                                    placeholder="Enter Claims",
                                                ),
                                                dbc.FormFeedback(valid=True),
                                                dbc.FormFeedback(
                                                    "Diagnosis claims must be a number",
                                                    valid=False,
                                                ),
                                            ]
                                        ),
                                        md={"size": 2, "order": 1},
                                    ),
                                    dbc.Col(
                                        dbc.FormGroup(
                                            [
                                                dbc.Label(
                                                    "Number of Procedures Per Year:",
                                                    html_for="px",
                                                ),
                                                dbc.Input(
                                                    type="integer",
                                                    id="px",
                                                    placeholder="Enter Procedures",
                                                ),
                                                dbc.FormFeedback(valid=True),
                                                dbc.FormFeedback(
                                                    "Number of procedures must be a number",
                                                    valid=False,
                                                ),
                                            ]
                                        ),
                                        md={"size": 2, "order": 2, "offset": 1},
                                    ),
                                    dbc.Col(
                                        dbc.FormGroup(
                                            [
                                                dbc.Label(
                                                    "Claims Outside of Primary Insurance:",
                                                    html_for="hcpcs",
                                                ),
                                                dbc.Input(
                                                    type="integer",
                                                    id="hcpcs",
                                                    placeholder="Enter Claims",
                                                ),
                                                dbc.FormFeedback(valid=True),
                                                dbc.FormFeedback(
                                                    "Claims must be a number",
                                                    valid=False,
                                                ),
                                            ]
                                        ),
                                        md={"size": 2, "order": 3, "offset": 1},
                                    ),
                                ],
                                align="end",
                                justify="center",
                            ),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            dbc.Row(
                                dbc.Col(
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Submit",
                                                color="primary",
                                                block=True,
                                                id="submit_val",
                                            ),
                                            dbc.Spinner(html.Div(id="loading")),
                                        ]
                                    ),
                                    md={"size": 3},
                                ),
                                justify="center",
                            ),
                            html.Br(),
                            html.Br(),
                            dbc.Alert(
                                [html.H4(id="output", style={"textAlign": "center"})],
                                color="dark",
                                is_open=False,
                                id="prediction_alert",
                                style={
                                    "display": "flex",
                                    "height": "120px",
                                    "align-items": "center",
                                    "justify-content": "center",
                                },
                            ),
                        ]
                    ),
                ),
            )
        )
    ]
)

app.title = "Healthcare Predictions"
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(
            id="page-content",
            children=[
                html.Div(navbar),
                html.Div(jumbotron),
                html.Div(form),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
            ],
            style={"overflow": "hidden"},
        ),
    ]
)


@app.callback(
    [Output("age", "valid"), Output("age", "invalid")], [Input("age", "value")]
)
def check_age(age):
    if age:
        is_number = age.isnumeric()
        return is_number, not is_number
    return False, False


@app.callback(
    [Output("state", "valid"), Output("state", "invalid")], [Input("state", "value")]
)
def check_state(state):
    if state:
        is_abbr = len(state) == 2
        return is_abbr, not is_abbr
    return False, False


@app.callback([Output("dx", "valid"), Output("dx", "invalid")], [Input("dx", "value")])
def check_dx(dx):
    if dx:
        is_number = dx.isnumeric()
        return is_number, not is_number
    return False, False


@app.callback([Output("px", "valid"), Output("px", "invalid")], [Input("px", "value")])
def check_px(px):
    if px:
        is_number = px.isnumeric()
        return is_number, not is_number
    return False, False


@app.callback(
    [Output("hcpcs", "valid"), Output("hcpcs", "invalid")], [Input("hcpcs", "value")]
)
def check_hcpcs(hcpcs):
    if hcpcs:
        is_number = hcpcs.isnumeric()
        return is_number, not is_number
    return False, False


@server.route("/api")
def api_reroute():
    return redirect("/api/")


@server.route("/404")
@server.errorhandler(404)
def page_not_found():
    return render_template("page_not_found.html"), 404


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return app.layout
    else:
        return dcc.Location(pathname="/404", id="404")


@app.callback(
    Output("loading", "children"),
    [Input("submit_val", "n_clicks")],
    state=[
        State("age", "valid"),
        State("gender", "value"),
        State("dx", "value"),
        State("px", "value"),
        State("hcpcs", "value"),
    ],
)
def toggle_loading(n_clicks, age, gender, dx, px, hcpcs):
    if n_clicks:
        if age is False:
            pass
        elif gender is None:
            pass
        elif dx not in (None, ""):
            try:
                int(dx)
            except Exception as e:
                pass
        elif px not in (None, ""):
            try:
                int(px)
            except Exception as e:
                pass
        elif hcpcs not in (None, ""):
            try:
                int(hcpcs)
            except Exception as e:
                pass
        else:
            time.sleep(3)
    return


@app.callback(
    Output("prediction_alert", "is_open"),
    [Input("output", "children")],
    [State("output", "is_open")],
)
def toggle_prediction(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("output", "children"),
    [Input("submit_val", "n_clicks")],
    state=[
        State("age", "value"),
        State("gender", "value"),
        State("race", "value"),
        State("state", "value"),
        State("conditions", "value"),
        State("dx", "value"),
        State("px", "value"),
        State("hcpcs", "value"),
    ],
)
def predict(n_clicks, age, gender, race, state, conditions, dx, px, hcpcs):
    if n_clicks is None:
        pass
    else:
        try:
            if age is None:
                raise Exception("Must input age")
            else:
                try:
                    age = int(age)
                except Exception as e:
                    raise Exception("Age must be a number")
            if gender is None:
                raise Exception("Gender must be Male or Female")
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
                if "alz" in conditions:
                    alzheimers = 1
                else:
                    alzheimers = 2
                if "hf" in conditions:
                    heart_failure = 1
                else:
                    heart_failure = 2
                if "kd" in conditions:
                    kidney_disease = 1
                else:
                    kidney_disease = 2
                if "cr" in conditions:
                    cancer = 1
                else:
                    cancer = 2
                if "copd" in conditions:
                    copd = 1
                else:
                    copd = 2
                if "depr" in conditions:
                    depression = 1
                else:
                    depression = 2
                if "dia" in conditions:
                    diabetes = 1
                else:
                    diabetes = 2
                if "hd" in conditions:
                    heart_disease = 1
                else:
                    heart_disease = 2
                if "ost" in conditions:
                    osteoporosis = 1
                else:
                    osteoporosis = 2
                if "art" in conditions:
                    arthritis = 1
                else:
                    arthritis = 2
                if "stk" in conditions:
                    stroke = 1
                else:
                    stroke = 2
            if dx in (None, ""):
                dx = 0
            else:
                try:
                    dx = int(dx)
                except Exception as e:
                    raise Exception("Diagnosis claims must be a number")
            if px in (None, ""):
                px = 0
            else:
                try:
                    px = int(px)
                except Exception as e:
                    raise Exception("Number of procedures must be a number")
            if hcpcs in (None, ""):
                hcpcs = 0
            else:
                try:
                    hcpcs = int(hcpcs)
                except Exception as e:
                    raise Exception(
                        "Claims outside of primary insurance must be a number"
                    )

            payload = {
                "age": age,
                "gender": gender,
                "race": race,
                "state": state,
                "alzheimers": alzheimers,
                "heart_failure": heart_failure,
                "kidney_disease": kidney_disease,
                "cancer": cancer,
                "copd": copd,
                "depression": depression,
                "diabetes": diabetes,
                "heart_disease": heart_disease,
                "osteoporosis": osteoporosis,
                "arthritis": arthritis,
                "stroke": stroke,
                "dx": dx,
                "px": px,
                "hcpcs": hcpcs,
            }

            response = requests.post(
                "http://34.102.187.98/api/prediction", json=payload, verify=True
            )

            dict_response = dict(response.json())

            if list(dict_response.keys())[0] == "prediction":
                return "Predicted Annual Responsibility Cost: ${}".format(
                    dict_response["prediction"]
                )
            else:
                return dict_response["error"]

        except Exception as e:
            logging.error(e)
            return "Error: {}".format(str(e))


if __name__ == "__main__":
    from waitress import serve

    serve(server, host="0.0.0.0", port="80")
