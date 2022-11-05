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

files = os.listdir(SRC_FOLDER_NAME)
states = [x[-10:-8] for x in files if x[-4:] == ".csv"]
fig, axs = plt.subplots(nrows=3, ncols=5)
fig.suptitle("Todos os Municípios - Histograma por votação")
fig.tight_layout()

bins = list(range(0, 105, 5))

print('\n\n Todos os municipios')
for j, state in enumerate(states):
    row, col = j//5, j%5

    tgt = TARGET % state
    df = pd.read_csv(SRC_FOLDER_NAME + tgt + "_bus.csv")
    df['pbolso'] = 100*df['bolso']/(df['bolso']+df['lula'])


    #print(len(dff))
    d2020 = df[df['tipo_urna']=="UE2020"]
    dist_2020 = 100*d2020['pbolso'].value_counts(bins=bins, sort=False) / len(d2020)

    dn2020 = df[df['tipo_urna']!="UE2020"]
    dist_n2020 = 100*dn2020['pbolso'].value_counts(bins=bins, sort=False) / len(dn2020)

    axs[row, col].plot(bins[:-1], dist_2020.values, color ='b', label ='UE2020')
    axs[row, col].plot(bins[:-1], dist_n2020.values, color ='r', label ='não UE2020')
    axs[row, col].set_xlabel("distribuição de urnas")
    axs[row, col].set_ylabel("votação bolsonaro")
    axs[row, col].set_title(state)
    axs[row, col].legend()
     


    