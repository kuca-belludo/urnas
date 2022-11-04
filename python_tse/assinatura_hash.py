import argparse
import hashlib
import logging
import os
import sys

import asn1tools


def verifica_hash(origem: str, resumo: bytes, conteudo: bytes) -> str:
    sha = hashlib.sha512()
    sha.update(conteudo)
    digest = sha.digest()

    if digest != resumo:
        return (False, f"{origem}: {digest.hex()}\nda assinatura: {resumo.hex()}")
    else:
        return (True, "OK")


def verifica_hash_arquivo(path: str, resumo: bytes) -> str:
    with open(path, "rb") as file:
        conteudo = file.read()

    return verifica_hash("do arquivo", resumo, conteudo)


def verifica_hashes_arquivos(dir_arqs: str, assinaturas: dict):
    erros = 0
    for assinaturaArquivo in assinaturas["arquivosAssinados"]:
        nome_arquivo = assinaturaArquivo["nomeArquivo"]
        path = os.path.join(dir_arqs, nome_arquivo)
        logging.info("Validando arquivo %s", nome_arquivo)

        if not os.path.isfile(path):
            logging.error("Arquivo não encontrado %s", nome_arquivo)
            erros += 1
            continue

        resumo = assinaturaArquivo["assinatura"]["hash"]
        res = verifica_hash_arquivo(path, resumo)
        if not res[0]:
            logging.error("Hash do arquivo %s está incorreto", nome_arquivo)
            print(f"{res[1]}")
            erros += 1

    return erros


def verifica_hashes_de(path: str, conv, envelope: dict, campo: str):
    entidade_assinatura = envelope[campo]
    assinaturas_encoded = entidade_assinatura["conteudoAutoAssinado"]

    erros = 0
    auto_hash = entidade_assinatura["autoAssinado"]["assinatura"]["hash"]
    res = verifica_hash("do conteúdo", auto_hash, assinaturas_encoded)
    if not res[0]:
        logging.error("Validando %s - hash do conteúdo do aruqivo de assinatura está incorreto", campo)
        print(f"{res[1]}")
        erros += 1
    else:
        logging.info("Validando %s - hash do conteúdo do aruqivo de assinatura está correto", campo)

    assinaturas_decoded = conv.decode("Assinatura", assinaturas_encoded)
    erros += verifica_hashes_arquivos(path, assinaturas_decoded)
    return erros


def verifica_hashes(asn1_paths: list, assinatura_path: str):
    conv = asn1tools.compile_files(asn1_paths, codec="ber", numeric_enums=True)
    with open(assinatura_path, "rb") as file:
        envelope_encoded = bytearray(file.read())
    envelope_decoded = conv.decode("EntidadeAssinaturaResultado", envelope_encoded)
    dir_arquivos = os.path.dirname(assinatura_path)
    erros = 0
    erros += verifica_hashes_de(dir_arquivos, conv, envelope_decoded, "assinaturaSW")
    erros += verifica_hashes_de(dir_arquivos, conv, envelope_decoded, "assinaturaHW")
    return erros


def main():
    parser = argparse.ArgumentParser(
        description="Le o arquivo de assinaturas da Urna Eletrônica (UE) e verifica os hashes dos arquivos de resultado",
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
            logging.error(
                "Arquivo de especificação das assinaturas (%s) não encontrado", asn1_path)
            sys.exit(-1)

    erros = verifica_hashes(asn1_paths, assinatura_path)

    if erros == 0:
        logging.info("Validação terminada com sucesso")
        sys.exit(0)
    else:
        logging.error("Validação terminada com erros")
        sys.exit(-1)


if __name__ == "__main__":
    main()
