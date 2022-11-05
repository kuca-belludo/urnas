#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arquivo que lê os boletins e tipos de urna e gera um dataframe. 
@author: kuka
"""


import asn1tools
import pandas as pd
import os

from conf import  DST_FOLDER_NAME

# processa um boletim de urna
def read_bus(conv, src_fldr):

    print("reading bus")
    
    flist = os.listdir(src_fldr)
    boletins = [x for x in flist if ".bu" in x]

    # lê cada boletim
    bus = {"boletim": [], "bolso":[], "lula": [], "branco": [], "nulo": []}
    for i, boletim in enumerate(boletins):

        # lê e decodifica boletim
        bu_path = src_fldr + boletim
        with open(bu_path, "rb") as file:
            envelope_encoded = bytearray(file.read())
        envelope_decoded = conv.decode("EntidadeEnvelopeGenerico", envelope_encoded)
        bu_encoded = envelope_decoded["conteudo"]
        del envelope_decoded["conteudo"]  # remove o conteúdo para não imprimir como array de bytes
        #print(envelope_decoded)
        bu_decoded = conv.decode("EntidadeBoletimUrna", bu_encoded)
        bu_decoded.keys()

        
        # a estrutura de dados é uma dicionário, de listas de dicionários de listas etc etc etc
        bolso, lula, nulo, branco = 0, 0, 0, 0
        for resultado in bu_decoded['resultadosVotacaoPorEleicao']:
            #print(resultado.keys())
            for res in resultado['resultadosVotacao']:
                if res['tipoCargo'] == 'majoritario':
                    for tot in res['totaisVotosCargo']:
                        #print (tot.keys())
                        #print(tot['codigoCargo'])
                        if tot['codigoCargo'][1] == 'presidente':
                            for votos in tot['votosVotaveis']:
                                #print(votos.keys())
                                if votos['tipoVoto'] == 'nominal' and votos['identificacaoVotavel']['partido'] == 22:
                                    bolso = votos['quantidadeVotos']
                                if votos['tipoVoto'] == 'nominal' and votos['identificacaoVotavel']['partido'] == 13:
                                    lula = votos['quantidadeVotos']
                                if votos['tipoVoto'] == 'nulo':
                                    nulo = votos['quantidadeVotos']
                                if votos['tipoVoto'] == 'branco':
                                    branco = votos['quantidadeVotos']

        # registra dados extraídos
        bus["boletim"].append(boletim)
        bus["bolso"].append(bolso)
        bus["lula"].append(lula)
        bus["branco"].append(branco)
        bus["nulo"].append(nulo)

        if i%2000 == 0:
            print(i, boletim, bolso, lula, branco, nulo)

    # retorna dados em forma de dataframe    
    return pd.DataFrame(bus)

def add_tipo_urna(df, models_fname):

    print("adicionando tipo")
    df["tipo_urna"] = "none"
    df.index = df["boletim"]

    with open(models_fname, "r") as fp:
        for i, line in enumerate(fp.readlines()):
            urna, tipo = line.split()
            urna = urna.split('.')[0]
            urna= urna + '.bu'
            if urna in df.index:
                df.at[urna, 'tipo_urna'] = tipo
    return df


def main():


    # estrutura do boletim (copiado dos scripts do TSE)
    asn1_paths = "../spec/bu.asn1"
    conv = asn1tools.compile_files(asn1_paths, codec="ber")

    SRC = '../generated_data/'
    content = os.listdir(SRC)
    txts = [x[:-11] for x in content if x[-11:] == "_models.txt"]
    csvs = [x[:-8] for x in content if x[-8:] == "_bus.csv"]
    must_proc = [x for x in txts if x not in csvs]

    for m_proc_fname in must_proc:

        src_fldr = "../downloaded_data/" + m_proc_fname + '/'
        models_fname = "../generated_data/" + m_proc_fname + '_models.txt'
        dst_fname = "../generated_data/" + m_proc_fname + "_bus.csv"
        
        # Lẽ conteúdo das urnas
        df = read_bus(conv, src_fldr)

        # adiciona informação do tipo de urna e salva dataframe
        df = add_tipo_urna(df, models_fname)
        df.to_csv(dst_fname)

if __name__ == "__main__":
    main()
