from dash import Dash, html, dcc, Input, Output, no_update
import dash_bootstrap_components as dbc
from dash import dash_table 
from math import floor


COR_PRIMARIA = "#DBC5AD"
COR_SECUNDARIA = "#EEE8E1"
COR_TERCIARIA = "#3F3A38"
CARD_HEIGHT=80

def create_card_col_component(card_id, card_size, card_display, config_graph):
    component_card_col_default = dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id=card_id, config=config_graph, style={'height': f'{CARD_HEIGHT}px' })
                                ], style={'color': 'blue !importtant'})
                            ], style={'height': '100%', 'display': card_display, 'border': f'1px solid {COR_TERCIARIA}', 'background-color': f'{COR_SECUNDARIA}'}),
                        ], sm=12, lg=card_size)
    return component_card_col_default



# def card_metrics(config_graph, todas_metricas, config_dash, origem_midia):
def card_metrics(config_graph, todas_metricas, dash_config, origem_midia):

    # metrica_origem_midia = metricas_origem_midia[origem_midia]
    # metrica_origem_midia = config_dash['origem_midia'][origem_midia]['cards']

    metrica_origem_midia = getattr(dash_config.origem_midia, origem_midia).cards


    getattr(dash_config.origem_midia, origem_midia).ordem = {
        card: idx for idx, card in enumerate(metrica_origem_midia)
    }

    # config_dash['origem_midia'][origem_midia]['ordem'] = {
    #     card: idx for idx, card in enumerate(config_dash['origem_midia'][origem_midia]['cards'])
    # }

    component_cards_list_origem_midia_tmp = []
    for metrica in todas_metricas:
        card = {}
        card['card_id'] = f'card-{metrica}_{origem_midia}'
        card['card_col_size'] = floor(12/len(metrica_origem_midia))
        if card['card_col_size'] < 1:
            card['card_col_size'] = 1
        # card['card_col_size'] = 2
        if metrica in (metrica_origem_midia):
            card['card_display'] = 'block'
        else:
            card['card_display'] = 'none'
        component_cards_list_origem_midia_tmp.append(card)


    none_display = [card for card in component_cards_list_origem_midia_tmp if card['card_display'] == 'none']
    block_display = [card for card in component_cards_list_origem_midia_tmp if card['card_display'] == 'block']

    def key_func(card):
        # Usa a ordem fornecida na chave 'ordem'
        card_id = card['card_id']
        metric = card_id.replace('card-', '').split('_')[0]
        # return config_dash['origem_midia'][origem_midia]['ordem'].get(metric, float('inf'))
        return getattr(dash_config.origem_midia, origem_midia).ordem.get(metric, float('inf'))

    # Ordena a lista usando a função de chave customizada
    block_display = sorted(block_display, key=key_func)

    # Concatena a lista mantendo a ordem original
    component_cards_list_origem_midia = block_display + none_display

    cards_origem_midia = [ create_card_col_component(card['card_id'], card['card_col_size'], card['card_display'], config_graph)  for card in component_cards_list_origem_midia]
    output_card_origem_midia_list = [Output(f'card-{metrica}_{origem_midia}', 'figure') for metrica in metrica_origem_midia]
    # output_card_origem_midia_list = [Output(f'card-{metrica}_{origem_midia}', 'figure') for metrica in todas_metricas]

    return cards_origem_midia, output_card_origem_midia_list



def lista_canal(lista_origem_midia):

    
    aux_lista_origem_midia = lista_origem_midia
    aux_lista_origem_midia.append('purchases')
    input_lista_canal = [Input(f'lista_canal_{origem_midia}', 'value') for origem_midia in aux_lista_origem_midia]
    output_lista_canal = [Output(f'lista_canal_{origem_midia}', 'options') for origem_midia in aux_lista_origem_midia]
    
    return input_lista_canal, output_lista_canal

def lista_trafego(lista_origem_midia):
    
    input_lista_trafego = [Input(f'lista_trafego_{origem_midia}', 'value') for origem_midia in lista_origem_midia]
    output_lista_trafego = [Output(f'lista_trafego_{origem_midia}', 'options') for origem_midia in lista_origem_midia]
    
    
    
    return input_lista_trafego, output_lista_trafego



def date_picker_range():
    input_date_picker = [Input('date-picker', 'start_date'), Input('date-picker', 'end_date')]
    return input_date_picker

def purchases_history():
    return dash_table.DataTable(
        id='table_purchases_history',
        
        style_cell_conditional=[
            {'if': {'column_id': 'data'},'textAlign': 'left'},
            {'if': {'column_id': 'categoria'},'textAlign': 'left'},
            {'if': {'column_id': 'produto'},'textAlign': 'left'},
            {'if': {'column_id': 'quantidade'},'textAlign': 'center'}
            ],
        style_data={'color': 'black','backgroundColor': 'white'},
        style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': COR_SECUNDARIA,}],
        style_header={
                    'backgroundColor': COR_TERCIARIA,
                    'color': COR_SECUNDARIA,
                    'fontWeight': 'bold',
                    'fontSize': '140%',
                    'textAlign': 'center'
                    }
    )


def purchases_category():
    return dash_table.DataTable(
        id='table_purchases_category',
        style_cell_conditional=[
            {'if': {'column_id': 'categoria'},'textAlign': 'left'},
            {'if': {'column_id': 'quantidade'},'textAlign': 'center'}
            ],
        style_data={'color': 'black','backgroundColor': 'white'},
        style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': COR_SECUNDARIA,}],
        style_header={
                    'backgroundColor': COR_TERCIARIA,
                    'color': COR_SECUNDARIA,
                    'fontWeight': 'bold',
                    'fontSize': '140%',
                    'textAlign': 'center'
                    }
    )