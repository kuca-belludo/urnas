import argparse
import logging
import os
import sys

import asn1tools


def espacos(profundidade: int):
    return ".   " * profundidade


def valor_membro(membro):
    if isinstance(membro, (bytes, bytearray)):
        return bytes(membro).hex()
    return membro


def print_list(lista: list, profundidade: int):
    indent = espacos(profundidade)
    for membro in lista:
        if type(membro) is dict:
            print_dict(membro, profundidade + 1)
        else:
            print(f"{indent}valor_membro(membro)")


def print_dict(entidade: dict, profundidade: int):
    for key in sorted(entidade):
        membro = entidade[key]
        print_membro(membro, key, profundidade)


def print_membro(membro, key, profundidade: int):
    indent = espacos(profundidade)
    if type(membro) is dict:
        print(f"{indent}{key}:")
        print_dict(membro, profundidade + 1)
    elif type(membro) is list:
        print(f"{indent}{key}: [")
        print_list(membro, profundidade + 1)
        print(f"{indent}] <== {key}")
    elif type(membro) is tuple:
        print_membro(membro[1], f"{key} ({membro[0]})", profundidade)
    else:
        print(f"{indent}{key} = {valor_membro(membro)}")


def processa_rdv(asn1_paths: list, rdv_path: str):
    conv = asn1tools.compile_files(asn1_paths, codec="ber")
    with open(rdv_path, "rb") as file:
        rdv_encoded = bytearray(file.read())
    rdv_decoded = conv.decode("EntidadeResultadoRDV", rdv_encoded)
    print_membro(rdv_decoded, "EntidadeResultadoRDV", 0)


def main():
    parser = argparse.ArgumentParser(
        description="Le o arquivo de Registro Digital do Voto (RDV) da Urna Eletrônica (UE) e imprime um extrato",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-a", "--asn1", nargs="+", required=True,
                        help="Caminho para o arquivo de especificação asn1 do RDV")
    parser.add_argument("-r", "--rdv", type=str, required=True,
                        help="Caminho para o arquivo de RDV originado na UE")
    parser.add_argument("--debug", action="store_true", help="ativa o modo DEBUG do log")

    args = parser.parse_args()

    rdv_path = args.rdv
    asn1_paths = args.asn1
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info("Converte %s com as especificações %s", rdv_path, asn1_paths)
    if not os.path.exists(rdv_path):
        logging.error("Arquivo do RDV (%s) não encontrado", rdv_path)
        sys.exit(-1)
    for asn1_path in asn1_paths:
        if not os.path.exists(asn1_path):
            logging.error("Arquivo de especificação do RDV (%s) não encontrado", asn1_path)
            sys.exit(-1)

    processa_rdv(asn1_paths, rdv_path)


if __name__ == "__main__":
    main()
