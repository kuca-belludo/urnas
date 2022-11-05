
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Este arquivo lê os logs e gera um arquivo texto com os modelos das urnas.
@author: kuka
"""

import py7zr
import codecs
import os

from conf import DST_FOLDER_NAME


# Para cada log, descompacta, encontra a string "Modelo de Urna" e extrai e retorna o modelo de urna encontrado
#fname = SRC_FOLDER_NAME
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
    SRC = '../downloaded_data/'
    DST = '../generated_data/'
    content = os.listdir(SRC)
    outp = os.listdir(DST)
    folds = [x for x in content if os.path.isfile(SRC+x) == False]
    must_proc = [x for x in folds if x + '_models.txt' not in outp]
    
    for f in must_proc:
        SRC_FOLDER_NAME = SRC+f + '/'
    
        # lê todos os arquivos e filtra os que tem a extensão .logjez
        flist = os.listdir(SRC_FOLDER_NAME)
        logs = [x for x in flist if ".logjez" in x]
        print("num logs: ", len(logs))


        # lista com a saída
        logrel = []
        for i, logf in enumerate(logs):
            ver = get_versao_urna(SRC_FOLDER_NAME + logf)
            logrel.append((logf, ver))
            if i % 2000 == 0:
                print(i, (logf, ver))
    
        # remove arquivos que por ventura possam ter sido criados    
        print('remove files')
        garbage = os.listdir(".")
        garbage = [x for x in garbage if ".jez" in x]
        for f_del in garbage:
            os.remove(f_del)
        
        # cria um arquivo de saída e coloca os dados lá
        with open(DST_FOLDER_NAME + f + '_models.txt', 'w') as fp:
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


