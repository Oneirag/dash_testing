# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import logging

def main():
    # Disable Flask's get/post console logs
    log = logging.getLogger('werkzeug')
    #log.disabled = True

    app = dash.Dash()
    app.config['suppress_callback_exceptions'] = True
    app.scripts.config.serve_locally = True

    app.layout = html.Div(children=[
        html.Div([
            html.Button('Get', className="info-button", n_clicks=0, id='info-button'),
        ], className="info-button-div"),
        ##### DETAILED INFO MODAL ######
        html.Div([
            html.Div([
                html.Label('JUST SOME TEXT: ')
            ], className="text-div"),
            html.Div([
                html.Button('Close', className="close-button", n_clicks=0, id='close-button'),
            ], className="close-button-div"),
        ], className="modal-container", id="modal-container", style={'display': 'none'}),
        ##### MODAL BACKDROP ######
        html.Div([
        ], className="modal-backdrop", id="modal-backdrop", style={'display': 'none'}),
        html.Div(id='modal-button-values', children="Get:0 Close:0 last:Close", style={'display': 'none'}),
    ])

    ###########################
    ###### MODAL CONTROL ######
    ###########################

    @app.callback(Output('modal-button-values', 'children'),
        [Input('info-button', 'n_clicks'), Input('close-button', 'n_clicks')],
        [State('modal-button-values', 'children')],[])
    def modal_button_status(get_clicks, close_clicks, button_values):
        button_values = dict([i.split(':') for i in button_values.split(' ')])

        if get_clicks > int(button_values["Get"]):
            last_clicked = "Get"
        elif close_clicks > int(button_values["Close"]):
            last_clicked = "Close"
        else:
            last_clicked = "Close"

        return "Get:{0} Close:{1} last:{2}".format(get_clicks, close_clicks, last_clicked)

    @app.callback(Output('modal-container', 'style'),
        [Input('modal-button-values', 'children')],
        [],[])
    def modal_display_status(button_values):
        button_values = dict([i.split(':') for i in button_values.split(' ')])

        if button_values["last"] == 'Get':
            return {'display': 'inline'}
        else:
            return {'display': 'none'}

    @app.callback(Output('modal-backdrop', 'style'),
        [Input('modal-button-values', 'children')],
        [],[])
    def modal_backdrop_status(button_values):
        button_values = dict([i.split(':') for i in button_values.split(' ')])

        if button_values["last"] == 'Get':
            return {'display': 'inline'}
        else:
            return {'display': 'none'}

    external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                    "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                    "https://codepen.io/cryptocss/pen/geyPdg.css",
                    "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",]

    for css in external_css:
        app.css.append_css({"external_url": css})

    app.run_server(debug=False)

if __name__ == '__main__':
    main()