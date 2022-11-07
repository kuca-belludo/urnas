#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: kuca
"""
import pandas as pd
import matplotlib.pyplot as plt

plt.close('all')

#load planilha cerimedo, filter and opend ceara votes
votos = pd.read_csv("../planilha_cerimedo/VOTOS_T1E2.csv", skiprows=1, sep=';')
locais = pd.read_csv("../downloaded_data/eleitorado_local_votacao_2022.csv", sep=';', encoding = "ISO-8859-1")

if 1:
    locais['ID_SECAO'] = locais['SG_UF'] + '_' + locais['CD_MUNICIPIO'].astype(str)  \
                + '_' + locais['NR_ZONA'].astype(str)  + '_' + locais['NR_SECAO'].astype(str) 
    locais = locais.drop_duplicates(subset=['ID_SECAO'])

    locf = locais[['ID_SECAO', 'NR_LATITUDE', 'NR_LONGITUDE']]
    
    nvotos = pd.merge(votos, locf, on='ID_SECAO', how='left')

    len(locais), len(locf), len(votos), len(nvotos)

# plot all locations
if 1: 
    vt = nvotos
    import geopandas as gpd

    infos_ufs = gpd.read_file('../downloaded_data/bcim_2016_21_11_2018.gpkg', layer='lim_unidade_federacao_a')
    fig, ax = plt.subplots()
    infos_ufs.plot(ax=ax)
    ax.plot(vt['NR_LONGITUDE'], vt['NR_LATITUDE'], 'ro', label='URNAS')
    ax.legend()
    ax.set_title('Mapa de urnas')
    
# low abstention places
if 1:
    vt['pbolso'] = 100*vt['T2QT22']/(vt['T2QT22'] + vt['T2QT13'])    
    vt['plula'] = 100*vt['T2QT13']/(vt['T2QT22'] + vt['T2QT13'])    
    
    vt['ABST'] = 100 - 100*vt['T1QTTOT']/vt['T1QTAPTOS']

    # split ballot models
    da = vt[vt['ABST'] < 5]
    len(da)
    print(da['pbolso'].mean())
    print(da['plula'].mean())

# high concentration places
if 1:

    db = vt[vt['pbolso'] > 95]
    len(db)    
    dl = vt[vt['plula'] > 95]
    len(dl)    

    fig, ax = plt.subplots()
    infos_ufs.plot(ax=ax)
    ax.plot(db['NR_LONGITUDE'], db['NR_LATITUDE'], 'bo', label='Alta vot bolso')
    ax.plot(dl['NR_LONGITUDE'], dl['NR_LATITUDE'], 'ro', label='Alta vot lula')
    ax.legend()
    ax.set_title('Mapa de alta votação')
