import argparse
import logging
import os
import sys

import asn1tools


def extrai_certificado_de(nome_certificado: str, conv, modelo: int, entidade_assinatura: dict):
    if not "certificadoDigital" in entidade_assinatura:
        logging.error("certificadoDigital não encontrado na assinatura")
        sys.exit(-1)

    certificado = entidade_assinatura["certificadoDigital"]
    nome = nome_certificado + ".pem" if modelo == 20 else nome_certificado + ".der"
    logging.info("Criando certificado %s", nome)
    with open(nome, "wb") as file:
        file.write(certificado)


def extrai_certificado(asn1_paths: list, assinatura_path: str, nome_certificado: str):
    conv = asn1tools.compile_files(asn1_paths, codec="ber", numeric_enums=True)
    with open(assinatura_path, "rb") as file:
        envelope_encoded = bytearray(file.read())
    envelope_decoded = conv.decode("EntidadeAssinaturaResultado", envelope_encoded)
    modelo = envelope_decoded["modeloUrna"]
    entidade_assinatura = envelope_decoded["assinaturaHW"]

    extrai_certificado_de(nome_certificado, conv, modelo, entidade_assinatura)


def main():
    parser = argparse.ArgumentParser(
        description="Le o arquivo de assinaturas da Urna Eletrônica (UE) e extrai o certificado",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-a", "--asn1", nargs="+", required=True,
                        help="Caminho para o arquivo de especificação asn1 das assinaturas")
    parser.add_argument("-s", "--assinatura", type=str, required=True,
                        help="Caminho para o arquivo de assinatura originado na UE")
    parser.add_argument("-o", "--output", type=str, required=True,
                        help="Caminho para o arquivo de certificado (sem extensão)")
    parser.add_argument("--debug", action="store_true", help="ativa o modo DEBUG do log")

    args = parser.parse_args()

    assinatura_path = args.assinatura
    asn1_paths = args.asn1
    nome_certificado = args.output
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

    extrai_certificado(asn1_paths, assinatura_path, nome_certificado)


if __name__ == "__main__":
    main()
