import argparse
import copy
import logging
import os
import sys

import asn1tools


def espacos(profundidade: int):
    return ".   " * profundidade


def valor_membro(membro):
    if isinstance(membro, (bytes, bytearray)):
        if len(membro) > 80:
            return bytes(membro[:80]).hex() + " ..."
        else:
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


def print_entidade_assinatura(entidade_assinatura: dict, name: str, profundidade: int, conv):
    # copiado para evitar que seja impresso como binário
    conteudo = copy.copy(entidade_assinatura["conteudoAutoAssinado"])
    # deleta o campo porque ele será impresso decodificado
    del entidade_assinatura["conteudoAutoAssinado"]
    print_membro(entidade_assinatura, name, profundidade)
    assinatura = conv.decode("Assinatura", conteudo)
    print_membro(assinatura, "conteudoAutoAssinado", profundidade + 1)


def processa_assinaturas(asn1_paths: list, assinatura_path: str):
    conv = asn1tools.compile_files(asn1_paths, codec="ber")
    with open(assinatura_path, "rb") as file:
        envelope_encoded = bytearray(file.read())
    envelope_decoded = conv.decode("EntidadeAssinaturaResultado", envelope_encoded)
    assinatura_sw = copy.copy(envelope_decoded["assinaturaSW"])
    assinatura_hw = copy.copy(envelope_decoded["assinaturaHW"])
    # remove o conteúdo para não imprimir como array de bytes
    del envelope_decoded["assinaturaSW"]
    del envelope_decoded["assinaturaHW"]

    print_membro(envelope_decoded, "EntidadeResultadoRDV", 0)
    print_entidade_assinatura(assinatura_sw, "Assinatura SW", 1, conv)
    print_entidade_assinatura(assinatura_hw, "Assinatura HW", 1, conv)


def main():
    parser = argparse.ArgumentParser(
        description="Le o arquivo de assinaturas da Urna Eletrônica (UE) e imprime seu conteúdo",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-a", "--asn1", nargs="+", required=True,
                        help="Caminho para o arquivo de especificação asn1 das assinaturas")
    parser.add_argument("-s", "--assinatura", type=str, required=True,
                        help="Caminho para o arquivo de assinatura originado na UE")
    parser.add_argument("--debug", action="store_true", help="ativa o modo DEBUG do log")

    args = parser.parse_args()

    assinatura_path = args.assinatura
    asn1_paths = args.asn1
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info("Processa %s com as especificações %s", assinatura_path, asn1_paths)
    if not os.path.exists(assinatura_path):
        logging.error("Arquivo de assinaturas (%s) não encontrado", assinatura_path)
        sys.exit(-1)
    for asn1_path in asn1_paths:
        if not os.path.exists(asn1_path):
            logging.error("Arquivo de especificação das assinaturas (%s) não encontrado", asn1_path)
            sys.exit(-1)

    processa_assinaturas(asn1_paths, assinatura_path)


if __name__ == "__main__":
    main()
