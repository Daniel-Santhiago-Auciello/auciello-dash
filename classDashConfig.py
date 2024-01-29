


import pandas as pd
from math import floor
pd.options.mode.chained_assignment = None  # default='warn'

import pandas_gbq
from google.oauth2 import service_account
from plotly.subplots import make_subplots
from plotly import graph_objects as go
from datetime import date, datetime, timedelta

config_dash_dict = {
    'origem_midia' : {
        'total' : 
            {
            'cards' : [
                    'compras',
                    'receita',
                    'ticket',
                    'investimento',
                    'roas-real',
                    'roas-minimo',
                    'roas-ideal',
                    'taxa-conversao'
                ] 
            },
        'google_ads': 
            {
            'cards' : [
                'compras',
                'receita',
                'ticket',
                'investimento',
                'cliques',
                'ctr',
                'cpm',
                'cpa',
                'roas-real',
                'roas-minimo',
                'roas-ideal',
                'taxa-conversao',
            ],
            'filter_field' : 'canal',
            'filter_value' : 'Google Ads',
        },
        'google_organic' : 
            {
            'cards' : [
                    'impressoes',
                    'ctr',
                    'compras',
                    'receita',
                    'ticket',
                    'taxa-conversao',     
                ],
            'filter_field' : 'trafego',
            'filter_value' : 'google organic', 
            },
        'facebook_ads': 
            {
            'cards' : [
                'cpm',
                'impressoes',
                'ctr',
                'cliques',
                'cpc',
                'adicao-carrinho',
                'inicio-checkout',
                'compras',
                'receita',
                'ticket',
                'investimento',
                'roas-real',

            ],
            'filter_field' : 'canal',
            'filter_value' : 'Facebook Ads', 
        },
        'direct' : 
            {
            'cards' : [
                    'compras',
                    'receita',
                    'ticket',
                    'taxa-conversao',
                ],
            'filter_field' : 'canal',
            'filter_value' : 'Direct', 
            },
        'referral' : 
            {
            'cards' : [
                    'compras',
                    'receita',
                    'ticket',
                    'taxa-conversao',
                ],
            'filter_field' : 'canal',
            'filter_value' : 'Referral', 
            }, 
    },
    'formulas':{
        'compras': 'round(sum(compras),0)' ,
        'receita': 'round(sum(receita_final) ,2)' ,
        'ticket': 'round(sum(receita_final) / sum(compras),2)' , 
        'investimento': 'round(sum(media_cost) ,2)' , 
        'cliques': 'round(sum(clicks) ,2)',
        'impressoes': 'round(sum(impressions) ,2)',
        'cpm': 'round(sum(media_cost) / sum(impressions) * 1000 ,2)' , 
        'cpa': 'round(sum(media_cost) / sum(compras) ,2)',
        'cpc': 'round(sum(media_cost) / sum(clicks) ,2)',
        'ctr': 'round(sum(clicks) / sum(impressions) * 100 ,2)',
        'adicao-carrinho': 'round(sum(add_to_cart) ,2)',
        'inicio-checkout': 'round(sum(begin_checkout) ,2)',
        'roas-real': 'round(sum(receita_final) / sum(media_cost),2)' , 
        'roas-minimo': 'round(sum(receita_final) / sum(lucro_final),2)' , 
        'roas-ideal': 'round(sum(receita_final) / sum(valor_caixa),2)' , 
        'taxa-conversao': 'round(sum(compras) / sum(session_start) * 100 ,2)' , 
    },
    'prefix':{
        'compras':          "",
        'receita':          "R$",
        'ticket':           "R$",
        'investimento':     "R$",
        'cliques':          "",
        'impressoes':       "",
        'cpm':              "R$", 
        'cpa':              "R$", 
        'cpc':              "R$",
        'ctr':              "",
        'adicao-carrinho':  "",
        'inicio-checkout':  "",
        'roas-real':        "",
        'roas-minimo':      "",
        'roas-ideal':       "",
        'taxa-conversao':   "",
    },
    'suffix':{
        'compras':          "",
        'receita':          "",
        'ticket':           "",
        'investimento':     "",
        'cliques':          "",
        'impressoes':       "",
        'cpm':              "", 
        'cpa':              "", 
        'cpc':              "",
        'ctr':              "%",
        'adicao-carrinho':  "",
        'inicio-checkout':  "",
        'roas-real':        "",
        'roas-minimo':      "",
        'roas-ideal':       "",
        'taxa-conversao':   "%",
    },
    'mapeamento_funil_order_by': {
        'impressions': 1, 
        'clicks': 2, 
        'session_start': 3, 
        'view_item': 4, 
        'add_to_cart': 5, 
        'begin_checkout': 6, 
        'compras': 7
    },
    'mapeamento_funil_passos': {
        'impressions': 'Impressões', 
        'clicks': 'Cliques', 
        'session_start': 'Início de Sessão', 
        'view_item': 'Visualização de Produto', 
        'add_to_cart': 'Adições ao Carrinho', 
        'begin_checkout': 'Início de Checkout', 
        'compras': 'Compras'
    }
}
class DashConfig:
    def __init__(self, config_dash_dict, is_top_level=True):
        # Atribui cada chave-valor do dicionário como atributo da classe
        for chave, valor in config_dash_dict.items():
            if isinstance(valor, dict):
                # Se o valor for um dicionário, crie uma instância da classe correspondente a esse dicionário
                setattr(self, chave, DashConfig(valor, is_top_level=False))
            else:
                setattr(self, chave, valor)
        # Adiciona a credencial apenas no nível superior da classe
        if is_top_level:
            self.credentials = service_account.Credentials.from_service_account_file('auciello-design-aed7e8fab9d8.json')
    def bq_get_total_metrics(self):
        query = '''
            SELECT distinct
                base_date,
                canal,
                trafego,
                SUM(impressions) as impressions,
                SUM(media_cost) as media_cost,
                SUM(clicks) as clicks,

                SUM(session_start)  as session_start,
                SUM(view_item)  as view_item,
                SUM(add_to_cart)  as add_to_cart,
                SUM(begin_checkout)  as begin_checkout,
                SUM(compras) as compras,
                SUM(receita_final) as receita_final,

                SUM(custo_final) as custo_final,
                SUM(lucro_final) as lucro_final,
                SUM(valor_caixa) as valor_caixa,
            FROM 
                `auciello-design.mart.ga4_total_funnel`
            WHERE
                1=1
            GROUP BY 
                base_date,
                canal,
                trafego
        '''
        self.df = pandas_gbq.read_gbq(
            query,
            project_id='auciello-design',
            credentials = self.credentials,
            dialect='standard'
        )
        self.df['base_date'] = pd.to_datetime(self.df['base_date'], format='%Y-%m-%d')
        return self.df
    def bq_get_purchases(self):
        query = '''
            with
            cte_purchases as (
                SELECT 
                    DATE(base_datetime) as base_date,
                    canal,
                    trafego,
                    item_id,
                    item_category as categoria,
                    item_name as produto,
                    sum(quantity) as quantidade
                FROM
                    `auciello-design.mart.ga4_purchase_sessions`
                where 
                    1=1
                group by 
                    1,2,3,4,5,6
                order by 
                    1 desc
            )
            , cte_gmc as (
                SELECT  DISTINCT
                    offer_id as item_id,
                    TRIM(REGEXP_EXTRACT(product_type, r'[^>]+$')) as product_category,
                FROM
                    `auciello-design.gmc_transfer.Products_641108502`
                WHERE
                    1=1
                QUALIFY 
                    ROW_NUMBER() OVER (PARTITION BY offer_id, TIMESTAMP_TRUNC(_PARTITIONTIME, DAY) ) = 1
                    AND  ROW_NUMBER() OVER (PARTITION BY offer_id ORDER BY product_data_timestamp DESC ) = 1
                ORDER BY 
                    offer_id desc
            )
            SELECT 
                cte_purchases.base_date,
                cte_purchases.canal,
                cte_purchases.trafego,
                cte_gmc.product_category as categoria,
                cte_purchases.produto,
                cte_purchases.quantidade
                from cte_purchases 
                left join cte_gmc using(item_id)
            ORDER BY
                cte_purchases.base_date DESC
        '''
        self.df_purchases = pandas_gbq.read_gbq(
            query,
            project_id='auciello-design',
            credentials = self.credentials,
            dialect='standard'
        )
        self.df_purchases['base_date'] = pd.to_datetime(self.df_purchases['base_date'], format='%Y-%m-%d')
        return self.df_purchases
    def bq_get_filtered_metrics(self, filter_field = '', filter_value= ''):
        if filter_field != '':
            df_filtered = self.df[self.df[filter_field] == filter_value]
        else:
            df_filtered = self.df
        return df_filtered
    def unpivot_analytics_metrics(self, filter_field = '', filter_value= ''):
        if filter_field != '':
            df_filtered = self.df[self.df[filter_field] == filter_value]
        else:
            df_filtered = self.df
        df_melt = pd.melt(df_filtered, 
                        id_vars=['base_date','canal','trafego'], 
                        # value_vars=['session_start','add_to_cart','begin_checkout','compras'], 
                        value_vars=['session_start','view_item','add_to_cart','begin_checkout','compras'], 
                        var_name='step', 
                        value_name='values'
                    )
        df_melt['base_date'] = pd.to_datetime(df_melt['base_date'], format='%Y-%m-%d')
        # df_melt.drop_duplicates(inplace=True)
        return df_melt
    def unpivot_impressions_and_analytics_metrics(self, filter_field = '', filter_value= ''):
        if filter_field != '':
            df_filtered = self.df[self.df[filter_field] == filter_value]
        else:
            df_filtered = self.df
        df_melt = pd.melt(df_filtered, 
                        id_vars=['base_date','trafego'], 
                        # value_vars=['impressions','session_start','add_to_cart','begin_checkout','compras'], 
                        value_vars=['impressions','clicks','session_start','view_item', 'add_to_cart','begin_checkout','compras'], 
                        var_name='step', 
                        value_name='values'
                    )
        df_melt['base_date'] = pd.to_datetime(df_melt['base_date'], format='%Y-%m-%d')
        # df_melt.drop_duplicates(inplace=True)
        return df_melt
    def get_list_origem_midia(self):
        self.lista_origem_midia = list(self.origem_midia.__dict__.keys())
        return self.lista_origem_midia
    def get_list_formulas(self):
        return list(self.formulas.__dict__.keys())
    def get_dataframes_origem_midia(self):
        dfs_origem_midia = {}
        dfs_melt_origem_midia = {}
        for origem_midia in self.lista_origem_midia:
            # dash_config.origem_midia
            if origem_midia != 'total':
                filter_field = getattr(dash_config.origem_midia, origem_midia).filter_field
                filter_value = getattr(dash_config.origem_midia, origem_midia).filter_value
                dfs_origem_midia[origem_midia] = dash_config.bq_get_filtered_metrics(
                    filter_field = filter_field, 
                    filter_value= filter_value
                    )
                if origem_midia in ('google_ads','google_organic','facebook_ads'):
                    dfs_melt_origem_midia[origem_midia] = dash_config.unpivot_impressions_and_analytics_metrics(
                        filter_field = filter_field, 
                        filter_value= filter_value
                        )
                else:
                    dfs_melt_origem_midia[origem_midia] = dash_config.unpivot_analytics_metrics(
                        filter_field = filter_field, 
                        filter_value= filter_value
                        )
            elif origem_midia == 'total':
                dfs_origem_midia['total'] = dash_config.bq_get_total_metrics()
                dfs_melt_origem_midia['total'] = dash_config.unpivot_analytics_metrics(
                    filter_field = '', 
                    filter_value= ''
                    )
        dfs_origem_midia['purchases'] = dash_config.bq_get_purchases()
        return dfs_origem_midia, dfs_melt_origem_midia 

# print(dfs_origem_midia)





dash_config = DashConfig(config_dash_dict)


# getattr(dash_config.origem_midia, origem_midia_variavel).cards

