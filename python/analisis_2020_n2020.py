#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: kuka
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

SRC_FOLDER_NAME = "../generated_data/"

tipos =  ['UE2009', 'UE2010', 'UE2011', 'UE2013', 'UE2015', 'UE2020']
TARGET = "bu_imgbu_logjez_rdv_vscmr_2022_2t_%s"
THRESHOLD = 100e3

files = os.listdir(SRC_FOLDER_NAME)
states = [x[-10:-8] for x in files if x[-4:] == ".csv"]

# votes per ballot (votos por urna)
vtpb = {'st':[], 'UE2020':[], 'nUE2020':[]}

print(f"\n\n municipios até {THRESHOLD:0,.0f} votos válidos")
for state in states:
    print("="*30)
    print(state)
    print("modelo", '\t', '# urnas', '\t', '% bolso')
    tgt = TARGET % state
    df = pd.read_csv(SRC_FOLDER_NAME + tgt + "_bus.csv")
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
    vtpb['st'].append(state)
    d2020 = dff[dff['tipo_urna']=="UE2020"]
    med_bolso_2020 = 100*d2020['bolso'].sum()/(d2020['bolso'].sum()+d2020['lula'].sum())
    print ('UE2020', '\t', len(d2020), '\t\t', "%.1f"%med_bolso_2020)

    dn2020 = dff[dff['tipo_urna']!="UE2020"]
    med_bolso_n2020 = 100*dn2020['bolso'].sum()/(dn2020['bolso'].sum()+dn2020['lula'].sum())
    print ('nUE2020', '\t', len(dn2020), '\t\t', "%.1f"%med_bolso_n2020)

    
    
    vtpb['UE2020'].append(med_bolso_2020)
    vtpb['nUE2020'].append(med_bolso_n2020)

if 1:

    # set width of bar
    barWidth = 0.25
    fig, ax = plt.subplots(figsize =(12, 8))
    fig.suptitle(f"municipios até {THRESHOLD:0,.0f} votos válidos")
     
    # Set position of bar on X axis
    br1 = np.arange(len(states))
    br2 = [x + barWidth for x in br1]
     
    # Make the plot
    plt.bar(br1, vtpb['nUE2020'], color ='r', width = barWidth,
            edgecolor ='grey', label ='nao UE2020')
    plt.bar(br2, vtpb['UE2020'], color ='b', width = barWidth,
            edgecolor ='grey', label ='UE2020')
     
    # Adding Xticks
    plt.xlabel('Estados', fontweight ='bold', fontsize = 15)
    plt.ylabel('% média vot do bolsonaro por tipo de urna', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(states))], states)
     
    plt.legend()


    