
from dash import Dash, html, dcc, Input, Output, no_update
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO, load_figure_template
# from dash_table import DataTable
from dash import dash_table 






# dbc_cards = {}
# output_card = []
# for origem_midia in lista_origem_midia:
#     globals()[f"cards_{origem_midia}"], globals()[f"output_card_{origem_midia}_list"] = card_metrics(config_graph, todas_metricas, config_dash, origem_midia)
#     dbc_cards[origem_midia] = globals()[f"cards_{origem_midia}"]
#     output_card.append( globals()[f"output_card_{origem_midia}_list"] )





# tab_total =  dbc.Container(children=[

#                 # Linha 1 - Filtros
#                 dbc.Row([
#                     dbc.Col([
#                         html.H5('Escolha o Canal'),
#                         dcc.Dropdown(id='lista_canal_total',  value='Todos Valores', multi=False)
#                     ], sm=6, lg=6),
#                     dbc.Col([
#                         html.H5('Escolha o Tráfego'),
#                         dcc.Dropdown(id='lista_trafego_total',  value='Todos Valores', multi=False)
#                     ], sm=6, lg=6),
#                 ], className='g-2 my-auto', style={'margin-top': '7px'}),

#                 # Linha 2 - Cards
#                 dbc.Row( dbc_cards['total'] , className='g-2 my-auto', style={'margin-top': '7px'}),
#                 # Linha 3 - Gráficos
#                 dbc.Row([
#                     dbc.Col([
#                         dcc.Graph(id='funil_conversao_total', className='dbc', config=config_graph, style={'height': '500px'}),
#                     ], sm=12, lg=9),
#                     dbc.Col([
#                             dcc.Graph(id='barra_compras_mensal_total', className='dbc', config=config_graph, style={'height': '200px'}),
#                             dcc.Graph(id='linha_taxa_conversao_mensal_total', className='dbc', config=config_graph, style={'height': '300px'})      
#                     ], sm=12, lg=3)
#                 ], className='g-2 my-auto', style={'margin-top': '7px'}),

#                 # Linha 4 - Gráficos

#                 # dbc.Row([
#                 #     dbc.Col([
#                 #         dcc.Graph(id='linha_taxa_conversao_mensal_total', className='dbc', config=config_graph)
#                 #     ], sm=12, lg=12)
#                 # ], className='g-2 my-auto', style={'margin-top': '7px'})


#             ], fluid=True, style={'height': '100vh'})

# tab_google_ads =  dbc.Container(children=[
#                 # Linha 1 - Filtros
#                 dbc.Row([
#                     dbc.Col([
#                         html.H5('Escolha o Canal'),
#                         dcc.Dropdown(id='lista_canal_google_ads',  value='Todos Valores', multi=False)
#                     ], sm=6, lg=6),
#                     dbc.Col([
#                         html.H5('Escolha o Tráfego'),
#                         dcc.Dropdown(id='lista_trafego_google_ads',  value='Todos Valores', multi=False)
#                     ], sm=6, lg=6),
#                 ], className='g-2 my-auto', style={'margin-top': '7px'}),
#                 # Linha 2 - Cards
#                 dbc.Row(dbc_cards['google_ads'] , className='g-2 my-auto', style={'margin-top': '7px'}),
                
#                 # Linha 3 - Gráficos
#                 dbc.Row([
#                     dbc.Col([
#                         dcc.Graph(id='funil_conversao_google_ads', className='dbc', config=config_graph, style={'height': '500px'})
#                     ], sm=12, lg=9),
#                     dbc.Col([
#                         dcc.Graph(id='barra_compras_mensal_google_ads', className='dbc', config=config_graph, style={'height': '200px'}),
#                         dcc.Graph(id='linha_taxa_conversao_mensal_google_ads', className='dbc', config=config_graph, style={'height': '300px'}) 
#                     ], sm=12, lg=3)
#                 ], className='g-2 my-auto', style={'margin-top': '7px'})
#             ], fluid=True, style={'height': '100vh'})



# tab_google_organic =  dbc.Container(children=[

#                 # Linha 1 - Filtros
#                 dbc.Row([
#                     dbc.Col([
#                         html.H5('Escolha o Canal'),
#                         dcc.Dropdown(id='lista_canal_google_organic',  value='Todos Valores', multi=False)
#                     ], sm=6, lg=6),
#                     dbc.Col([
#                         html.H5('Escolha o Tráfego'),
#                         dcc.Dropdown(id='lista_trafego_google_organic',  value='Todos Valores', multi=False)
#                     ], sm=6, lg=6),
#                 ], className='g-2 my-auto', style={'margin-top': '7px'}),

#                 # Linha 2 - Cards
#                 dbc.Row( dbc_cards['google_organic'] , className='g-2 my-auto', style={'margin-top': '7px'}),
                
#                 # Linha 3 - Gráficos
#                 dbc.Row([
#                     dbc.Col([
#                         dcc.Graph(id='funil_conversao_google_organic', className='dbc', config=config_graph, style={'height': '500px'})
#                     ], sm=12, lg=9),
#                     dbc.Col([
#                         dcc.Graph(id='barra_compras_mensal_google_organic', className='dbc', config=config_graph, style={'height': '200px'}),
#                         dcc.Graph(id='linha_taxa_conversao_mensal_google_organic', className='dbc', config=config_graph, style={'height': '300px'}) 
#                     ], sm=12, lg=3)
#                 ], className='g-2 my-auto', style={'margin-top': '7px'})
#             ], fluid=True, style={'height': '100vh'})

# tab_facebook_ads =  dbc.Container(children=[
#                 # Linha 1 - Filtros
#                 dbc.Row([
#                     dbc.Col([
#                         html.H5('Escolha o Canal'),
#                         dcc.Dropdown(id='lista_canal_facebook_ads',  value='Todos Valores', multi=False)
#                     ], sm=6, lg=6),
#                     dbc.Col([
#                         html.H5('Escolha o Tráfego'),
#                         dcc.Dropdown(id='lista_trafego_facebook_ads',  value='Todos Valores', multi=False)
#                     ], sm=6, lg=6),
#                 ], className='g-2 my-auto', style={'margin-top': '7px'}),
#                 # Linha 2 - Cards
#                 dbc.Row(dbc_cards['facebook_ads'] , className='g-2 my-auto', style={'margin-top': '7px'}),
                
#                 # Linha 3 - Gráficos
#                 dbc.Row([
#                     dbc.Col([
#                         dcc.Graph(id='funil_conversao_facebook_ads', className='dbc', config=config_graph, style={'height': '500px'})
#                     ], sm=12, lg=9),
#                     dbc.Col([
#                         dcc.Graph(id='barra_compras_mensal_facebook_ads', className='dbc', config=config_graph, style={'height': '200px'}),
#                         dcc.Graph(id='linha_taxa_conversao_mensal_facebook_ads', className='dbc', config=config_graph, style={'height': '300px'}) 
#                     ], sm=12, lg=3)
#                 ], className='g-2 my-auto', style={'margin-top': '7px'})
#             ], fluid=True, style={'height': '100vh'})

# tab_direct =  dbc.Container(children=[

#                 # Linha 1 - Filtros
#                 dbc.Row([
#                     dbc.Col([
#                         html.H5('Escolha o Canal'),
#                         dcc.Dropdown(id='lista_canal_direct',  value='Todos Valores', multi=False)
#                     ], sm=6, lg=6),
#                     dbc.Col([
#                         html.H5('Escolha o Tráfego'),
#                         dcc.Dropdown(id='lista_trafego_direct',  value='Todos Valores', multi=False)
#                     ], sm=6, lg=6),
#                 ], className='g-2 my-auto', style={'margin-top': '7px'}),

#                 # Linha 2 - Cards
#                 dbc.Row( dbc_cards['direct'] , className='g-2 my-auto', style={'margin-top': '7px'}),
#                 # Linha 3 - Gráficos
#                 dbc.Row([
#                     dbc.Col([
#                         dcc.Graph(id='funil_conversao_direct', className='dbc', config=config_graph, style={'height': '500px'})
#                     ], sm=12, lg=9),
#                     dbc.Col([
#                         dcc.Graph(id='barra_compras_mensal_direct', className='dbc', config=config_graph, style={'height': '200px'}),
#                         dcc.Graph(id='linha_taxa_conversao_mensal_direct', className='dbc', config=config_graph, style={'height': '300px'}) 
#                     ], sm=12, lg=3)
#                 ], className='g-2 my-auto', style={'margin-top': '7px'})
#             ], fluid=True, style={'height': '100vh'})

# tab_referral =  dbc.Container(children=[

#                 # Linha 1 - Filtros
#                 dbc.Row([
#                     dbc.Col([
#                         html.H5('Escolha o Canal'),
#                         dcc.Dropdown(id='lista_canal_referral',  value='Todos Valores', multi=False)
#                     ], sm=6, lg=6),
#                     dbc.Col([
#                         html.H5('Escolha o Tráfego'),
#                         dcc.Dropdown(id='lista_trafego_referral',  value='Todos Valores', multi=False)
#                     ], sm=6, lg=6),
#                 ], className='g-2 my-auto', style={'margin-top': '7px'}),
#                 # Linha 2 - Cards
#                 dbc.Row( dbc_cards['referral'] , className='g-2 my-auto', style={'margin-top': '7px'}),
#                 # Linha 3 - Gráficos
#                 dbc.Row([
#                     dbc.Col([
#                         dcc.Graph(id='funil_conversao_referral', className='dbc', config=config_graph, style={'height': '500px'})
#                     ], sm=12, lg=9),
#                     dbc.Col([
#                         dcc.Graph(id='barra_compras_mensal_referral', className='dbc', config=config_graph, style={'height': '200px'}),
#                         dcc.Graph(id='linha_taxa_conversao_mensal_referral', className='dbc', config=config_graph, style={'height': '300px'}) 
#                     ], sm=12, lg=3)
#                 ], className='g-2 my-auto', style={'margin-top': '7px'})
#             ], fluid=True, style={'height': '100vh'})


# tab_purchases = dbc.Container(children=[
#                     dbc.Row([
#                         dbc.Col([
#                             html.H5('Escolha o Canal'),
#                             dcc.Dropdown(id='lista_canal_purchases',  value='Todos Valores', multi=False),
#                         ], sm=11, lg=6),
#                         dbc.Col([
#                             html.H5('Escolha o Tráfego'),
#                             dcc.Dropdown(id='lista_trafego_purchases',  value='Todos Valores', multi=False)
#                         ], sm=6, lg=6),
#                     ], className='g-2 my-auto', style={'margin-top': '7px'}),
#                     dbc.Row([
#                         dbc.Col([
#                             html.H5('Histórico de Vendas'),
#                             dash_table.DataTable(id='table_purchases',)

#                         ], sm=11, lg=6),
#                         # dbc.Col([
#                         #     html.H5('Escolha o Tráfego'),
#                         #     dcc.Dropdown(id='lista_trafego_referral',  value='Todos Valores', multi=False)
#                         # ], sm=6, lg=6),
#                     ], className='g-2 my-auto', style={'margin-top': '7px'}),

#         ], fluid=True, style={'height': '100vh'}

# )