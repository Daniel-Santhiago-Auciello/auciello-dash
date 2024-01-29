# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc, Input, Output, no_update
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO, load_figure_template
# from dash_table import DataTable
from dash import dash_table 

from dash.dash_table.Format import Format, Scheme


import plotly.express as px
import pandas as pd
from math import floor
pd.options.mode.chained_assignment = None  # default='warn'

import pandas_gbq
from google.oauth2 import service_account
from plotly.subplots import make_subplots
from plotly import graph_objects as go
from datetime import date, datetime, timedelta

import calendar
import locale

locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')

# from extract_data import *
from custom_components import *

from app import *

from classDashConfig import *


# ========== Load ============ #


dash_config = DashConfig(config_dash_dict)


lista_origem_midia = dash_config.get_list_origem_midia()
todas_metricas = dash_config.get_list_formulas()

dfs_origem_midia, dfs_melt_origem_midia = dash_config.get_dataframes_origem_midia()


# ========== Styles ============ #
tab_card = {'height': '100%'}

COR_PRIMARIA = "#DBC5AD"
COR_SECUNDARIA = "#EEE8E1"
COR_TERCIARIA = "#3F3A38"

CARD_HEIGHT=80
CARD_NUMBER_SIZE = 26
CARD_TITLE_SIZE_PERCENT = 200

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor":"top", 
                "y":0.9, 
                "xanchor":"left",
                "x":0.1,
                "title": {"text": None},
                "font" :{"color":"white"},
                "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l":10, "r":10, "t":10, "b":10}
}

tab_style = {
    "background": COR_SECUNDARIA,
    'text-transform': 'uppercase',
    'color': COR_TERCIARIA,
    'border': COR_TERCIARIA,
    'font-size': '25px',
    'font-weight': 600,
    'font-family': 'Montserrat,-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif',
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '4px',
    'border-style': 'solid',
    'border-width': 'thin',
    'padding':'6px',
    'margin-right':'1px'
}

tab_selected_style = {
    "background": COR_TERCIARIA,
    'text-transform': 'uppercase',
    'color': COR_SECUNDARIA,
    'font-size': '25px',
    'font-weight': 600,
    'font-family': 'Montserrat,-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif',
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '4px',
    'padding':'6px',
    'margin-right':'1px'
}

config_graph={"displayModeBar": False, "showTips": False}


# template_theme1 = "flatly"
# template_theme2 = "darkly"

# template_theme1 = "minty"
# template_theme2 = "darkly"

# url_theme1 = dbc.themes.FLATLY
# url_theme2 = dbc.themes.DARKLY

# url_theme1 = dbc.themes.MINTY
# url_theme2 = dbc.themes.DARKLY

data_atual = datetime.now().date()
default_start_date = (date.today()-timedelta(days=90)).isoformat()



# =========== Criação de Card e Output de Card ============== #

dbc_cards = {}
output_card = []
for origem_midia in lista_origem_midia:
    # globals()[f"cards_{origem_midia}"], globals()[f"output_card_{origem_midia}_list"] = card_metrics(config_graph, todas_metricas, config_dash, origem_midia)
    globals()[f"cards_{origem_midia}"], globals()[f"output_card_{origem_midia}_list"] = card_metrics(config_graph, todas_metricas, dash_config, origem_midia)
    dbc_cards[origem_midia] = globals()[f"cards_{origem_midia}"]
    output_card.append( globals()[f"output_card_{origem_midia}_list"] )


# =========== Criação de Input e Output de Lista Canal Dropdown ============== #

input_lista_canal, output_lista_canal = lista_canal(lista_origem_midia)



# =========== Criação de Input e Output de Lista Tráfego Dropdown ============== #

input_lista_trafego, output_lista_trafego = lista_trafego(lista_origem_midia)

# =========== Criação de Input e Output de Date Picker ============== #

input_date_picker = date_picker_range()

# ======= Component Functions ======== #

def calculate_metrica_on_df(df_result, dash_config, metrica):

    variaveis_locais = {coluna: df_result[coluna] for coluna in df_result.columns}

    try:
        resultado = eval(getattr(dash_config.formulas, metrica), {}, variaveis_locais)
    except:
        resultado = None
    return resultado


def cards(campaign_value, start_date, end_date, selected_tab):

    # trafego = selected_tab
    # df = globals()[f"df_{trafego}"]
    df = dfs_origem_midia[selected_tab]
    # df_melt = globals()[f"df_{selected_tab}_melt"]
    df_melt = dfs_melt_origem_midia[selected_tab]
    metricas = getattr(dash_config.origem_midia, selected_tab).cards
    mask = (df['base_date'] >= start_date) & (df['base_date'] <= end_date)
    df_result = df.loc[mask]

    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    # end_date_dt = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%f")
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

    delta_days = (end_date_dt - start_date_dt).days


    previous_start_date = start_date_dt - timedelta(days=delta_days)
    previous_end_date = end_date_dt - timedelta(days=delta_days)
    previous_mask = (df['base_date'] >= previous_start_date) & (df['base_date'] <= previous_end_date)
    df_previous_result = df.loc[previous_mask]


    if campaign_value != "Todos Valores":
        df_result = df_result[df_result['trafego'] == campaign_value]
        df_previous_result = df_previous_result[df_previous_result['trafego'] == campaign_value]

    results = []
    for metrica in metricas:
        underline_metrica = metrica.replace('-','_')
        nome_variavel =  f'figure_card_{underline_metrica}'

        globals()[nome_variavel] = go.Figure()
        globals()[nome_variavel].add_trace(go.Indicator(
            mode='number+delta',
            # mode='number',
            title = 
            {"text": f"<span style='font-size:{CARD_TITLE_SIZE_PERCENT}%;'>{metrica.title()}</span><br>"},

            value = calculate_metrica_on_df(df_result, dash_config, metrica),
            delta = {
                'reference' : calculate_metrica_on_df(df_previous_result, dash_config, metrica),
                'relative': True,
                'valueformat': '.1%',
                },
            number = {
                        'prefix': getattr(dash_config.prefix, metrica), 
                        'suffix': getattr(dash_config.suffix, metrica), 
                        'font': {'size': CARD_NUMBER_SIZE}},
        
        ))

        globals()[nome_variavel].update_layout(paper_bgcolor = f'{COR_SECUNDARIA}')
        # globals()[nome_variavel].update_layout(main_config, height=CARD_HEIGHT)
        # globals()[nome_variavel].update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})

        results.append(globals()[nome_variavel])
    return results 

def funil_conversao(dash_config, campaign_value, start_date, end_date, selected_tab):
    # trafego = selected_tab.replace('tab-', '').replace('-','_')
    # trafego = selected_tab
    df = dfs_origem_midia[selected_tab]
    # df = globals()[f"df_{selected_tab}"]
    # df_melt = globals()[f"df_{selected_tab}_melt"]
    df_melt = dfs_melt_origem_midia[selected_tab]
    mask = (df_melt['base_date'] >= start_date) & (df_melt['base_date'] <= end_date)
    df_result = df_melt.loc[mask]

    df_result['order_by'] = df_result['step'].map(dash_config.mapeamento_funil_order_by.__dict__)
    df_result['passos'] = df_result['step'].map(dash_config.mapeamento_funil_passos.__dict__)
    
    if campaign_value != "Todos Valores":
        df_result = df_result[df_result['trafego'] == campaign_value]

    df_result_grouped = df_result.groupby(['step','order_by','passos'])['values'].sum().reset_index()
    df_result_grouped = df_result_grouped.sort_values(by='order_by')
    

    # Criação dos percentuais do Funil de Conversão
    # df_result_grouped['ratio_values_temp'] = df_result_grouped['values'] / df_result_grouped['values'].shift(1)
    # df_result_grouped['ratio_values'] = df_result_grouped['ratio_values_temp'].apply(lambda x: f'{x*100:.2f}%' if pd.notna(x) else 'NaN')

    fig_funil_conversao = go.Figure(go.Funnel(
        y=df_result_grouped['passos'],
        x=df_result_grouped['values'],
        marker = {'color': COR_PRIMARIA},

        textinfo="value+percent previous",
        texttemplate='%{value:,.2d}<br>%{percentPrevious:.2%}',
    ))
    # Configurando layout
    fig_funil_conversao.update_layout(
        main_config,
       title={
            'text': "Funil de Conversão",
            'x': 0.5,  # Define a posição horizontal do título no centro
            'y': 0.95,  # Define a posição vertical do título no topo (0.5 seria o meio)
            'xanchor': 'center',  # Ancora o título no centro horizontal
            'yanchor': 'top'  # Ancora o título no topo
        }
        # template=url_theme1,
    )
    fig_funil_conversao.update_layout({"margin": {"l":0, "r":0, "t":40, "b":0}})
    return fig_funil_conversao


def grafico_barras_compras_mensal(trafego_value, start_date, end_date, selected_tab):

    df = dfs_origem_midia[selected_tab]
    mask = (df['base_date'] >= start_date) & (df['base_date'] <= end_date)
    df_result = df.loc[mask]

    if trafego_value != "Todos Valores":
        df_result = df_result[df_result['trafego'] == trafego_value]

    df_result['base_month_order'] = df_result['base_date'].dt.strftime('%Y-%m')
    df_result['base_month_name'] = df_result['base_date'].dt.strftime('%b/%Y')

    df_result_grouped = df_result.groupby(['base_month_order','base_month_name'])['compras'].sum().reset_index()
    df_result_grouped = df_result_grouped.sort_values(by='base_month_order')

    figure = go.Figure(go.Bar(
                    x = df_result_grouped['base_month_name'],
                    y = df_result_grouped['compras'],
                    text = df_result_grouped['compras'],
                    textposition='auto',
                    textfont=dict(color=COR_TERCIARIA),
                    marker=dict(color=COR_PRIMARIA)
                ))

    figure.update_layout(
        main_config,
        title={
            'text': "Compras",
            'x': 0.5,  # Define a posição horizontal do título no centro
            'y': 0.95,  # Define a posição vertical do título no topo (0.5 seria o meio)
            'xanchor': 'center',  # Ancora o título no centro horizontal
            'yanchor': 'top'  # Ancora o título no topo
        },
        # template=url_theme1,
    )
    figure.update_layout({"margin": {"l":0, "r":0, "t":40, "b":0}})

    return figure

def grafico_linhas_taxa_conversao_mensal(trafego_value, start_date, end_date, selected_tab):

    # trafego = selected_tab
    # df = globals()[f"df_{trafego}"]
    df = dfs_origem_midia[selected_tab]
    mask = (df['base_date'] >= start_date) & (df['base_date'] <= end_date)
    df_result = df.loc[mask]

    if trafego_value != "Todos Valores":
        df_result = df_result[df_result['trafego'] == trafego_value]

    df_result['base_month_order'] = df_result['base_date'].dt.strftime('%Y-%m')
    df_result['base_month_name'] = df_result['base_date'].dt.strftime('%b/%Y')

    df_result_grouped = df_result.groupby(['base_month_order','base_month_name']).apply(lambda x: round( (x['compras'].sum() / x['session_start'].sum()) * 100 ,2 ))
    df_result_grouped.name = 'taxa-conversao'

    # Resetar o índice para obter um DataFrame
    df_result_grouped = df_result_grouped.reset_index()

    # df_result_grouped = df_result.groupby(['base_month_order','base_month_name'])['compras'].sum().reset_index()
    df_result_grouped = df_result_grouped.sort_values(by='base_month_order')

    figure = go.Figure(go.Scatter(
                    x=df_result_grouped['base_month_name'],
                    y=df_result_grouped['taxa-conversao'],
                    mode='lines+markers',  # Especifica que queremos uma linha e marcadores
                    line=dict(color=COR_PRIMARIA),
                    marker=dict(color=COR_PRIMARIA, size=10),
                    text=df_result_grouped['taxa-conversao'].apply(lambda x: f'{x}%'),  # Converte para formato percentual
                    # textposition='top center',  # Posição do texto em relação aos marcadores
                    # texttemplate='%{y}',
                    textfont=dict(color=COR_TERCIARIA),
                ))
    
    # Adicionar rótulos diretamente ao gráfico
    for i, value in enumerate(df_result_grouped['taxa-conversao']):
        figure.add_annotation(
            x=df_result_grouped['base_month_name'][i],
            y=value + 0.02,
            text=f'{value:.2}%',
            # textposition='outside',
            showarrow=False,
            font=dict(color=COR_TERCIARIA)
        )

    # figure.update_traces(
    #     texttemplate="%{x}"
    # )

    figure.update_layout(
        main_config,
        title={
            'text': "Taxa de Conversão por mês",
            'x': 0.5,  # Define a posição horizontal do título no centro
            'y': 0.95,  # Define a posição vertical do título no topo (0.5 seria o meio)
            'xanchor': 'center',  # Ancora o título no centro horizontal
            'yanchor': 'top'  # Ancora o título no topo
        },
        xaxis=dict(title='Mês'),
        yaxis=dict(title='Taxa de Conversão'),
        # template=url_theme1,
    )
    figure.update_layout({"margin": {"l":0, "r":0, "t":40, "b":0}})

    return figure



def get_table_purchases_history(df_purchases, canal_value, trafego_value, start_date, end_date):

    mask = (df_purchases['base_date'] >= start_date) & (df_purchases['base_date'] <= end_date)
    df_purchases = df_purchases.loc[mask]

    df_purchases['data'] = df_purchases['base_date'].dt.strftime('%d/%m/%Y')
    if canal_value != "Todos Valores":
        df_purchases = df_purchases[df_purchases['canal'] == canal_value]
    if trafego_value != "Todos Valores":
        df_purchases = df_purchases[df_purchases['trafego'] == trafego_value]

    df_purchases_table = df_purchases.copy()
    df_purchases_table = df_purchases_table.drop('base_date', axis=1)

    df_purchases_table = df_purchases_table[['data','categoria','produto','quantidade']]

    columns=[ {'name': col.title(), 
               'id': col}
             for col in df_purchases_table.columns
             ]
    data = df_purchases_table.to_dict('records')

    return [columns, data]


def get_table_purchases_category(df_purchases, canal_value, trafego_value, start_date, end_date):

    mask = (df_purchases['base_date'] >= start_date) & (df_purchases['base_date'] <= end_date)
    df_purchases = df_purchases.loc[mask]

    df_purchases['data'] = df_purchases['base_date'].dt.strftime('%d/%m/%Y')
    if canal_value != "Todos Valores":
        df_purchases = df_purchases[df_purchases['canal'] == canal_value]
    if trafego_value != "Todos Valores":
        df_purchases = df_purchases[df_purchases['trafego'] == trafego_value]

    df_purchases_table = df_purchases.copy()
    df_purchases_table = df_purchases_table.drop('base_date', axis=1)

    df_purchases_table = df_purchases_table[['data','categoria','produto','quantidade']]

    df_purchases_category = df_purchases_table.groupby(['categoria'])['quantidade'].sum().reset_index()

    df_purchases_category = df_purchases_category.sort_values(by='quantidade', ascending=False)


    columns=[ {'name': col.title(), 
               'id': col}
             for col in df_purchases_category.columns
             ]
    data = df_purchases_category.to_dict('records')

    return [columns, data]

# =========  Layout  =========== #

lista_origem_midia = dash_config.get_list_origem_midia()

tab_canal = {}
for origem_midia in lista_origem_midia:
    tab_canal[origem_midia] = dbc.Container(children=[
                    # Linha 1 - Filtros
                    dbc.Row([
                        dbc.Col([
                            html.H5('Escolha o Canal'),
                            dcc.Dropdown(id=f'lista_canal_{origem_midia}',  value='Todos Valores', multi=False)
                        ], sm=6, lg=6),
                        dbc.Col([
                            html.H5('Escolha o Tráfego'),
                            dcc.Dropdown(id=f'lista_trafego_{origem_midia}',  value='Todos Valores', multi=False)
                        ], sm=6, lg=6),
                    ], className='g-2 my-auto', style={'margin-top': '7px'}),
                    # Linha 2 - Cards
                    dbc.Row( dbc_cards[origem_midia] , className='g-2 my-auto', style={'margin-top': '7px'}),
                    # Linha 3 - Gráficos
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id=f'funil_conversao_{origem_midia}', className='dbc', config=config_graph, style={'height': '500px'}),
                        ], sm=12, lg=9),
                        dbc.Col([
                                dcc.Graph(id=f'barra_compras_mensal_{origem_midia}', className='dbc', config=config_graph, style={'height': '200px'}),
                                dcc.Graph(id=f'linha_taxa_conversao_mensal_{origem_midia}', className='dbc', config=config_graph, style={'height': '300px'})      
                        ], sm=12, lg=3)
                    ], className='g-2 my-auto', style={'margin-top': '7px'}),
                ], fluid=True, style={'height': '100vh'})





tab_canal['purchases'] = dbc.Container(children=[
                    dbc.Row([
                        dbc.Col([
                            html.H5('Escolha o Canal'),
                            dcc.Dropdown(id='lista_canal_purchases',  value='Todos Valores', multi=False),
                        ], sm=11, lg=6),
                        dbc.Col([
                            html.H5('Escolha o Tráfego'),
                            dcc.Dropdown(id='lista_trafego_purchases',  value='Todos Valores', multi=False)
                        ], sm=6, lg=6),
                    ], className='g-2 my-auto', style={'margin-top': '7px'}),
                    dbc.Row([
                        dbc.Col([
                            html.H5('Histórico de Vendas'),
                            purchases_history()
                        ], sm=11, lg=6, style={'margin-right':'0px', 'width': '49%'}),

                        dbc.Col([
                            html.H5('Top Categorias'),
                            purchases_category()
                        ], sm=11, lg=6, style={'margin-right':'0px', 'width': '49%'}),
                    ], className='d-flex justify-content-between', style={'margin-top': '7px'}),

        ], fluid=True, style={'height': '100vh'}

)

def create_tab_origem_midia(origem_midia):

    return dcc.Tab(label=origem_midia, value=origem_midia, style=tab_style, selected_style=tab_selected_style, children=[ tab_canal[origem_midia] ])

app.layout = dbc.Container(children=[
                dbc.Row([
                    dbc.Col([
                        html.Img(src="assets\\logos\\auciello-logo-brown.png", style={"float": "right", "width":"60%"}),
                        
                    ], sm=1, lg=1),
                    dbc.Col([
                        
                    ], sm=1, lg=2),
                    dbc.Col([
                        html.Legend(id='dashboard-title', children='Dashboard Insights - Auciello Design', 
                                    style={ "text-align": "center","width": "90%","left":"10%"}),
                    ], sm=8, lg=6),

                    dbc.Col([
                        # html.H5('Escolha o Período'),
                        dcc.DatePickerRange(id='date-picker', className='dbc align-items-center',
                            start_date=default_start_date, end_date=data_atual , display_format='DD/MM/YYYY',
                            )
                    ], sm=12, lg=3)
                    
                ], className='g-2 my-auto align-items-center', style={'margin-top': '7px'}),
                dcc.Tabs(id='tabs',  value='total',  children= (
                    [ create_tab_origem_midia(origem_midia) for origem_midia in lista_origem_midia ]
                +   [dcc.Tab(label='Compras', value='purchases', style=tab_style, selected_style=tab_selected_style, children=[ tab_canal['purchases']])]
                ) )
], fluid=True, style={'height': '100vh'})


# ======== Callbacks ========== #

#### == Callback Lista DropDown Canal == ####
@app.callback(
    output_lista_canal,
    input_date_picker,
)
def update_channel_options(start_date, end_date,):
    
    lista_canais = []
    origens_midia = ['total','google_ads','google_organic','facebook_ads','direct','referral','purchases']
    # origens_midia = ['total']
    for origem_midia in origens_midia:
        # mask = (globals()[f"df_{origem_midia}"]['base_date'] >= start_date) & (globals()[f"df_{origem_midia}"]['base_date'] <= end_date)
        mask = (dfs_origem_midia[origem_midia]['base_date']>= start_date) & (dfs_origem_midia[origem_midia]['base_date']<= end_date)
        # globals()[f"df_result_{origem_midia}"] = globals()[f"df_{origem_midia}"].loc[mask]
        globals()[f"df_result_{origem_midia}"] = dfs_origem_midia[origem_midia].loc[mask]
        globals()[f"opcoes_trafego_{origem_midia}"] = ['Todos Valores']
        globals()[f"opcoes_trafego_{origem_midia}"].extend(list(globals()[f"df_result_{origem_midia}"]['canal'].unique()))

        lista_canais.append(globals()[f"opcoes_trafego_{origem_midia}"])

    return lista_canais


#### == Callback Lista DropDown Trafego == ####
@app.callback(
    output_lista_trafego,
    input_date_picker
)
def update_traffic_options(start_date, end_date):
    

    lista_campanhas = []
    trafegos = ['total','google_ads','google_organic','facebook_ads','direct','referral','purchases']
    for trafego in trafegos:
        # mask = (globals()[f"df_{trafego}"]['base_date'] >= start_date) & (globals()[f"df_{trafego}"]['base_date'] <= end_date)
        mask = (dfs_origem_midia[trafego]['base_date']>= start_date) & (dfs_origem_midia[trafego]['base_date']<= end_date)
        # globals()[f"df_result_{trafego}"] = globals()[f"df_{trafego}"].loc[mask]
        globals()[f"df_result_{trafego}"] = dfs_origem_midia[trafego].loc[mask]
        globals()[f"opcoes_trafego_{trafego}"] = ['Todos Valores']
        globals()[f"opcoes_trafego_{trafego}"].extend(list(globals()[f"df_result_{trafego}"]['trafego'].unique()))

        lista_campanhas.append(globals()[f"opcoes_trafego_{trafego}"])


    return lista_campanhas



#### == Callback Funil de Conversão == ####

@app.callback(
    [
        Output('funil_conversao_total', 'figure'),
        Output('funil_conversao_google_ads', 'figure'),
        Output('funil_conversao_google_organic', 'figure'),
        Output('funil_conversao_facebook_ads', 'figure'),
        Output('funil_conversao_direct', 'figure'),
        Output('funil_conversao_referral', 'figure')
    ],
        input_date_picker,
        input_lista_trafego,
        
)
def callback_funil( start_date, end_date, 
                    *trafego_options
                    ):

    return_list = []
    for index, origem_midia in enumerate(lista_origem_midia):
        if origem_midia in ['total','google_ads','google_organic','facebook_ads','direct','referral']:
            return_list.append( funil_conversao(dash_config, trafego_options[index], start_date, end_date, selected_tab=origem_midia) )

    return return_list

#### == Callback Gráfico de Barras == ####

@app.callback(
    [
        Output('barra_compras_mensal_total', 'figure'),
        Output('barra_compras_mensal_google_ads', 'figure'),
        Output('barra_compras_mensal_google_organic', 'figure'),
        Output('barra_compras_mensal_facebook_ads', 'figure'),
        Output('barra_compras_mensal_direct', 'figure'),
        Output('barra_compras_mensal_referral', 'figure')
    ],
        input_date_picker,
        input_lista_trafego,
        
)
def callback_grafico_barras_compras( start_date, end_date,
                    *trafego_options
                    ):

    return_list = []
    for index, origem_midia in enumerate(lista_origem_midia):
        if origem_midia in ['total','google_ads','google_organic','facebook_ads','direct','referral']:
            return_list.append( grafico_barras_compras_mensal(trafego_options[index], start_date, end_date, selected_tab=origem_midia) )


    return return_list


#### == Callback Gráfico de Linhas  == ####

@app.callback(
    [
        Output('linha_taxa_conversao_mensal_total', 'figure'),
        Output('linha_taxa_conversao_mensal_google_ads', 'figure'),
        Output('linha_taxa_conversao_mensal_google_organic', 'figure'),
        Output('linha_taxa_conversao_mensal_facebook_ads', 'figure'),
        Output('linha_taxa_conversao_mensal_direct', 'figure'),
        Output('linha_taxa_conversao_mensal_referral', 'figure')
    ],
        input_date_picker,
        input_lista_trafego,
        
)
def callback_linhas_taxa_conversao( start_date, end_date,
                    *trafego_options
                    ):

    return_list = []
    for index, origem_midia in enumerate(lista_origem_midia):
        if origem_midia in ['total','google_ads','google_organic','facebook_ads','direct','referral']:
            return_list.append( grafico_linhas_taxa_conversao_mensal(trafego_options[index], start_date, end_date, selected_tab=origem_midia) )

    return return_list


#### == Callback Cards == ####
@app.callback(
    output_card,
    input_date_picker,
    input_lista_trafego,
)
def callback_cards( start_date, end_date,
                    *trafego_options
                   ):
    
    return_list = []
    for index, origem_midia in enumerate(lista_origem_midia):
        if origem_midia in ['total','google_ads','google_organic','facebook_ads','direct','referral']:
            return_list.append( cards(trafego_options[index], start_date, end_date, selected_tab=origem_midia) )

    return return_list


#### == Callback Table Purchases History == ####
@app.callback(
    # [
        Output('table_purchases_history', 'columns'),
        Output('table_purchases_history', 'data'),
    # ],
        input_date_picker,
        # input_lista_canal,
        # input_lista_trafego,
        Input('lista_canal_purchases', 'value'),
        Input('lista_trafego_purchases', 'value')
        
)
def callback_table_purchases_history( start_date, end_date,               
                    # *trafego_options
                    canal_options,
                    trafego_options
                    ):


    return get_table_purchases_history(dfs_origem_midia['purchases'], canal_options, trafego_options, start_date, end_date)

#### == Callback Table Purchases Category == ####
@app.callback(
    # [
        Output('table_purchases_category', 'columns'),
        Output('table_purchases_category', 'data'),
    # ],
        input_date_picker,
        # input_lista_canal,
        # input_lista_trafego,
        Input('lista_canal_purchases', 'value'),
        Input('lista_trafego_purchases', 'value')
        
)
def callback_table_purchases_category( start_date, end_date,               
                    # *trafego_options
                    canal_options,
                    trafego_options
                    ):


    return get_table_purchases_category(dfs_origem_midia['purchases'], canal_options, trafego_options, start_date, end_date)









if __name__ == '__main__':
    app.run_server(debug=True)


# if __name__ == '__main__':
#     app.run(debug=True)
