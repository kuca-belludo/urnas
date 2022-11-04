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

print(df)