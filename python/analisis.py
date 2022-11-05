#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: kuka
"""

import pandas as pd
import matplotlib.pyplot as plt
plt.close('all')

DST_FOLDER_NAME = "../generated_data/"


tipos =  ['UE2009', 'UE2010', 'UE2011', 'UE2013', 'UE2015', 'UE2020']
states = ["BA", "ES", "MG", "RS", "MS", 'MT']
TARGET = "bu_imgbu_logjez_rdv_vscmr_2022_2t_%s"
THRESHOLD = 100e3

print(f"\n\n municipios até {THRESHOLD:0,.0f} votos válidos")
for state in states:
    print("="*30)
    print(state)
    print("modelo", '\t', '# urnas', '\t', '% bolso')
    tgt = TARGET % state
    df = pd.read_csv(DST_FOLDER_NAME + tgt + "_bus.csv")
    df['pbolso'] = 100*df['bolso']/(df['bolso']+df['lula'])

    df['municipio'] = df['boletim'].str.slice(7, 12)
    ms = df.groupby('municipio')[['bolso','lula']].sum()
    ms['tot_val'] = ms['bolso']+ms['lula']
    ms = ms.sort_values('tot_val')
    
    # below 100k
    muns = ms[ms['tot_val']<THRESHOLD].index
    #print(len(muns))

    dff = df.loc[df['municipio'].isin(muns)]
    
    #print(len(dff))
    for tipo in tipos:
        dtip = dff[dff['tipo_urna']==tipo]
        print (tipo, '\t',len(dtip), '\t\t', "%.1f"%dtip['pbolso'].mean())

if 0:        
    fig, axes = plt.subplots(nrows=1, ncols=2)
    fig.suptitle(state)
    dff[dff['tipo_urna']=='UE2010'].plot.scatter('bolso', 'lula', ax=axes[0])
    dff[dff['tipo_urna']=='UE2020'].plot.scatter('bolso', 'lula', ax=axes[1])


    bins = list(range(0, 105, 5))
    dd = dff[dff['tipo_urna']=='UE2010']
    v0 = dd['pbolso'].value_counts(bins=bins, sort=False)
    v0 = 100*v0/v0.sum()
    dd = dff[dff['tipo_urna']=='UE2020']
    v1 = dd['pbolso'].value_counts(bins=bins, sort=False)
    v1 = 100*v1/v1.sum()

    fig, axes = plt.subplots(nrows=1, ncols=2)
    fig.suptitle(state)
    axes[0].plot(v0.values)
    axes[0].plot(v1.values)

    