#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: kuka
"""

import pandas as pd

DST_FOLDER_NAME = "../generated_data/"

df = pd.read_csv(DST_FOLDER_NAME + "bus.csv")

df[df['tipo_urna']=='UE2020'].plot.scatter('bolso', 'lula')
df[df['tipo_urna']!='UE2020'].plot.scatter('bolso', 'lula')

df['pbolso'] = 100*df['bolso']/(df['bolso']+df['lula'])
df['plula'] = 100*df['lula']/(df['bolso']+df['lula'])

dfa = df[df['tipo_urna']=='UE2020']
dfb = df[df['tipo_urna']!='UE2020']

print (dfa['pbolso'].mean())
print (dfb['pbolso'].mean())

print (dfa['plula'].mean())
print (dfb['plula'].mean())
