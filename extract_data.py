# import pandas as pd
# import pandas_gbq
# from google.oauth2 import service_account



# credentials = service_account.Credentials.from_service_account_file(
#     'auciello-design-aed7e8fab9d8.json')


# def get_total_metrics(credentials):

#     query = '''
#         SELECT distinct
#             base_date,
#             canal,
#             trafego,
#             SUM(impressions) as impressions,
#             SUM(media_cost) as media_cost,
#             SUM(clicks) as clicks,

#             SUM(session_start)  as session_start,
#             SUM(view_item)  as view_item,
#             SUM(add_to_cart)  as add_to_cart,
#             SUM(begin_checkout)  as begin_checkout,
#             SUM(compras) as compras,
#             SUM(receita_final) as receita_final,

#             SUM(custo_final) as custo_final,
#             SUM(lucro_final) as lucro_final,
#             SUM(valor_caixa) as valor_caixa,
#         FROM 
#             `auciello-design.mart.ga4_total_funnel`
#         WHERE
#             1=1
#         GROUP BY 
#             base_date,
#             canal,
#             trafego

#     '''

#     df = pandas_gbq.read_gbq(
#         query,
#         project_id='auciello-design',
#         credentials = credentials,
#         dialect='standard'
#     )

#     df['base_date'] = pd.to_datetime(df['base_date'], format='%Y-%m-%d')
    
#     return df


# def unpivot_analytics_metrics(df):

#     df_melt = pd.melt(df, 
#                     id_vars=['base_date','canal','trafego'], 
#                     # value_vars=['session_start','add_to_cart','begin_checkout','compras'], 
#                     value_vars=['session_start','view_item','add_to_cart','begin_checkout','compras'], 
#                     var_name='step', 
#                     value_name='values'
#                 )
#     df_melt['base_date'] = pd.to_datetime(df_melt['base_date'], format='%Y-%m-%d')
#     # df_melt.drop_duplicates(inplace=True)

#     return df_melt

# def unpivot_impressions_and_analytics_metrics(df):

#     df_melt = pd.melt(df, 
#                     id_vars=['base_date','trafego'], 
#                     # value_vars=['impressions','session_start','add_to_cart','begin_checkout','compras'], 
#                     value_vars=['impressions','clicks','session_start','view_item', 'add_to_cart','begin_checkout','compras'], 
#                     var_name='step', 
#                     value_name='values'
#                 )
#     df_melt['base_date'] = pd.to_datetime(df_melt['base_date'], format='%Y-%m-%d')
#     # df_melt.drop_duplicates(inplace=True)

#     return df_melt


# def get_purchases(credentials):

#     query = '''
#         SELECT 
#             DATE(base_datetime) as base_date,
#             canal,
#             trafego,
#             item_category as categoria,
#             item_name as produto,
#         FROM
#             `auciello-design.mart.ga4_purchase_sessions`
#         where 
#             1=1
#         order by 
#             base_datetime desc

#     '''

#     df = pandas_gbq.read_gbq(
#         query,
#         project_id='auciello-design',
#         credentials = credentials,
#         dialect='standard'
#     )

#     df['base_date'] = pd.to_datetime(df['base_date'], format='%Y-%m-%d')
    
#     return df
