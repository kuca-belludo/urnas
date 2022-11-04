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
    indent = espacos(profundidade)
    for key in sorted(entidade):
        membro = entidade[key]
        if type(membro) is dict:
            print(f"{indent}{key}:")
            print_dict(membro, profundidade + 1)
        elif type(membro) is list:
            print(f"{indent}{key}: [")
            print_list(membro, profundidade + 1)
            print(f"{indent}] <== {key}")
        else:
            print(f"{indent}{key} = {valor_membro(membro)}")


def processa_bu(asn1_paths: list, bu_path: str):
    conv = asn1tools.compile_files(asn1_paths, codec="ber")
    with open(bu_path, "rb") as file:
        envelope_encoded = bytearray(file.read())
    envelope_decoded = conv.decode("EntidadeEnvelopeGenerico", envelope_encoded)
    bu_encoded = envelope_decoded["conteudo"]
    del envelope_decoded["conteudo"]  # remove o conteúdo para não imprimir como array de bytes
    print("EntidadeEnvelopeGenerico:")
    print_dict(envelope_decoded, 1)
    bu_decoded = conv.decode("EntidadeBoletimUrna", bu_encoded)
    print("EntidadeBoletimUrna:")
    print_dict(bu_decoded, 1)


def main():
    parser = argparse.ArgumentParser(
        description="Converte um Boletim de Urna (BU) da Urna Eletrônica (UE) e imprime um extrato",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-a", "--asn1", nargs="+", required=True,
                        help="Caminho para o arquivo de especificação asn1 do BU")
    parser.add_argument("-b", "--bu", type=str, required=True,
                        help="Caminho para o arquivo de BU originado na UE")
    parser.add_argument("--debug", action="store_true", help="ativa o modo DEBUG do log")

    args = parser.parse_args()

    bu_path = args.bu
    asn1_paths = args.asn1
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info("Converte %s com as especificações %s", bu_path, asn1_paths)
    if not os.path.exists(bu_path):
        logging.error("Arquivo do BU (%s) não encontrado", bu_path)
        sys.exit(-1)
    for asn1_path in asn1_paths:
        if not os.path.exists(asn1_path):
            logging.error("Arquivo de especificação do BU (%s) não encontrado", asn1_path)
            sys.exit(-1)

    processa_bu(asn1_paths, bu_path)


if __name__ == "__main__":
    main()
