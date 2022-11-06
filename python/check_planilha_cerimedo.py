#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
credits: https://rodrigodutcosky.medium.com/mapas-coropl%C3%A9ticos-com-os-estados-do-brasil-em-python-b9b48c6db585

@author: kuca
"""
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

plt.close('all')

#load planilha cerimedo, filter and opend ceara votes
votos = pd.read_csv("../planilha_cerimedo/VOTOS_T1E2.csv", skiprows=1, sep=';')

##############################################################################
# Just checkin if cerimedo data is according to mine: using CEARA as example
##############################################################################
if 1: 
    vce = votos[votos['UF'] =='CE'].copy()
    orig = pd.read_csv("../generated_data/bu_imgbu_logjez_rdv_vscmr_2022_2t_CE_bus.csv")
    vce['names'] = vce['CD_MUNICIPIO'].astype(str).str.zfill(5) + \
                vce['NR_ZONA'].astype(str).str.zfill(4) + \
                vce['NR_SECAO'].astype(str).str.zfill(4)
    vce.index = vce['names']
    
    orig['names'] = orig['boletim'].str.slice(7, 20)
    orig.index = orig['names']
    
    # not found on local data, equal, different, missing cerimedo data
    nf, eq, df, ms = 0, 0, 0, 0
    for name in orig['names']:
        if name not in vce.index:
            nf += 1
        elif vce.loc[name, 'LOG_MODELO'] == orig.loc[name, 'tipo_urna']:
            eq += 1
        elif (vce.loc[name, 'LOG_MODELO'] != '-'):
                df += 1
        else:
            ms += 1
    print ("not found %d, equal: %d, different: %d, missing cerimedo: %d" % (nf, eq, df, ms))
    eq, df, ms = 100*eq/len(orig), 100*df/len(orig), 100*ms/len(orig)
    print ("equal: %.1f, different: %.1f, missing : %.1f" % (eq, df, ms))

##############################################################################
# plot pernambuco ballot histogram from cerimedo's data
##############################################################################
if 1: 
    bins = list(range(0, 105, 5))
    vrn = votos[votos['UF'] =='PE'].copy()
    vrn['pbolso'] = 100*vrn['T2QT22']/(vrn['T2QT22'] + vrn['T2QT13'])    
    
    d2020 = vrn[vrn['LOG_MODELO']=="UE2020"]
    dist_2020 = 100*d2020['pbolso'].value_counts(bins=bins, sort=False) / len(d2020)
    
    dn2020 = vrn[vrn['LOG_MODELO']!="UE2020"]
    dist_n2020 = 100*dn2020['pbolso'].value_counts(bins=bins, sort=False) / len(dn2020)
    
    fig, ax = plt.subplots()
    ax.plot(bins[:-1], dist_2020.values, 'b')
    ax.plot(bins[:-1], dist_n2020.values, 'r')
    ax.legend()
    ax.set_title('Histograma de urnas PE')


##############################################################################
# get ballots coordinates
##############################################################################
if 1:

    # load cerimedo data and vote location data
    vpe = votos[votos['UF'] =='PE'].copy()
    locais = pd.read_csv("../planilha_cerimedo/locaisCSV.csv")

    # I manually checked the municipalities are in the same order.
    muns_0 = sorted(set(vpe['NM_MUNICIPIO'].values))
    muns_1 = sorted(set(locais['Município'].values))

    mun_d = dict(zip(muns_1, muns_0))

    locais_d = {'mun_zn_sec': [], 'lat':[], 'lon': []}
    for loc_i in locais.index:
        loc = locais.loc[loc_i]
        for sec in loc['Seções'].split(','):
            sec = int(sec)
            zn = str(loc['Zona'])
            mun_zn_sec = mun_d[loc['Município']] + '_' + zn + '_' + str(sec)
            locais_d['mun_zn_sec'].append(mun_zn_sec)
            locais_d['lat'].append(loc['Latitude'])
            locais_d['lon'].append(loc['Longitude'])
    loc_df = pd.DataFrame(locais_d)
    loc_df.index = loc_df['mun_zn_sec']
    loc_df = loc_df.drop_duplicates()

    nf, fnd, vpe['lat'], vpe['lon'] = 0, 0, 0.0, 0.0
    print(len(vpe.index))
    for jj, idx in enumerate(vpe.index):
        mun, sec = vpe.loc[idx, 'NM_MUNICIPIO'], vpe.loc[idx, 'NR_SECAO']
        zn = str(int(vpe.loc[idx, 'NR_ZONA']))
        num_zn_sec = mun + '_' + zn + '_'+ str(int(sec))
        if num_zn_sec not in loc_df.index:
            nf += 1
        else:
            vpe.at[idx, 'lat']=loc_df.loc[num_zn_sec, 'lat']
            vpe.at[idx, 'lon']=loc_df.loc[num_zn_sec, 'lon']
            fnd += 1
    print(fnd, nf)

if 0:
    len(vpe[vpe['lat'] > -1])
    len(vpe[vpe['lat'] < -1])
    len(loc_df[loc_df['lat'] > -1])
    len(locais[locais['Latitude'] > -1])


##############################################################################
# plot ballots on map by type
##############################################################################
if 1:
    #load image mapa: https://www.ibge.gov.br/.
    #site: Geociências -> Downloads -> cartas_e_mapas -> bcim -> versao2016 — geopackage
    infos_ufs = gpd.read_file('../downloaded_data/bcim_2016_21_11_2018.gpkg', layer='lim_unidade_federacao_a')

    # split ballot models
    vpe['pbolso'] = 100*vpe['T2QT22']/(vpe['T2QT22'] + vpe['T2QT13'])    
    vpe_20 = vpe[vpe['LOG_MODELO'] == 'UE2020']
    vpe_n20 = vpe[vpe['LOG_MODELO'] != 'UE2020']
    len(vpe_20), len(vpe_n20)

    # plot models
    fig, ax = plt.subplots()
    infos_ufs.plot(ax=ax)
    ax.plot(vpe_20['lon'], vpe_20['lat'], 'go', label='UE2020')
    ax.plot(vpe_n20['lon'], vpe_n20['lat'], 'ro', label='nao UE2020')
    ax.legend()
    ax.set_title('Mapa de urnas PE')

    #######################################
    # filter ballots near coast
    vpe_20f = vpe_20[vpe_20['lon']>-35.140]
    vpe_n20f = vpe_n20[vpe_n20['lon']>-35.140]
    len(vpe_20f), len(vpe_n20f)
    
    # and plot again
    fig, ax = plt.subplots()
    infos_ufs.plot(ax = ax)
    ax.plot(vpe_20f['lon'], vpe_20f['lat'], 'yo', label='UE2020')
    ax.plot(vpe_n20f['lon'], vpe_n20f['lat'], 'mo', label='nao UE2020')
    ax.legend()
    ax.set_title('Mapa de urnas PE - Litoral')
    
    # finally plot the distrtibuition of coast ballots per type
    dist_2020 = 100*vpe_20f['pbolso'].value_counts(bins=bins, sort=False) / len(vpe_20f)
    dist_n2020 = 100*vpe_n20f['pbolso'].value_counts(bins=bins, sort=False) / len(vpe_n20f)
    
    fig, ax = plt.subplots()
    ax.plot(bins[:-1], dist_2020.values, 'y', label='UE2020')
    ax.plot(bins[:-1], dist_n2020.values, 'm', label='nao UE2020')
    ax.legend()
    ax.set_xlabel("distribuição de urnas")
    ax.set_ylabel("votação bolsonaro")
    ax.set_title('Histograma de urnas no litoral')
    