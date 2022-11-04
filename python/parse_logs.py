
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Este arquivo lê os logs e gera um arquivo texto com os modelos das urnas.
@author: kuka
"""

import py7zr
import codecs
import os

SRC_FOLDER_NAME = "../downloaded_data/bu_imgbu_logjez_rdv_vscmr_2022_2t_BA/"
DST_FOLDER_NAME = "../generated_data/"

# Para cada log, descompacta, encontra a string "Modelo de Urna" e extrai e retorna o modelo de urna encontrado
def get_versao_urna(fname):

    # extrai o arquivo 7z
    versao_urna = "None"
    with py7zr.SevenZipFile(fname, mode='r') as z:
        z.extractall()
        with codecs.open('logd.dat', 'r', encoding='utf-8', errors='ignore') as fp:
            for line in fp.readlines():

                # extrai a string e deleta o arquivo extraído (seria melhor usar uma biblioteca que já lê 
                # arquivos texto dentro de zips, mas meu linux tá meio bugado).
                if line.find("Modelo de Urna") != -1:
                    versao_urna = line.split()[-2]
                    break
        if os.path.isfile('logd.dat'):
            os.remove('logd.dat')
    return versao_urna


def main():
    # lê todos os arquivos e filtra os que tem a extensão .logjez
    flist = os.listdir(SRC_FOLDER_NAME)
    logs = [x for x in flist if ".logjez" in x]
    print("num logs: ", len(logs))

    # lista com a saída
    logrel = []
    for i, logf in enumerate(logs):
        ver = get_versao_urna(SRC_FOLDER_NAME + logf)
        logrel.append((logf, ver))
        if i % 1000 == 0:
            print(i, (logf, ver))

    # remove arquivos que por ventura possam ter sido criados    
    garbage = os.listdir(".")
    garbage = [x for x in garbage if ".jez" in x]
    for f in garbage:
        os.remove(f)
    
    
    # cria um arquivo de saída e coloca os dados lá
    with open(DST_FOLDER_NAME + 'models.txt', 'w') as fp:
        for item in logrel:
            fp.write("%s, %s\n" % (item[0], item[1]))
        print('Done')    

    # imprime a quantidade de urnas de cada modelo
    modelos = [x[1] for x in logrel]
    mod_set = set(modelos)
    for mod in mod_set:
        print(mod, len([x for x in modelos if x == mod]))

if __name__ == "__main__":
    main()


