import argparse
import hashlib
import logging
import os
import sys

import asn1tools
import ed25519


def valida_assinatura_votavel(verificador: ed25519.VerifyingKey, carga: str, codigoCargo: int, votosVotavel: dict):
    tipoVoto = votosVotavel["tipoVoto"]
    qtdVotos = votosVotavel["quantidadeVotos"]
    assinatura = votosVotavel["assinatura"]
    if tipoVoto in (1, 4):
        ident = votosVotavel["identificacaoVotavel"]
        partido = ident["partido"]
        codigo = ident["codigo"]
        descricao = f"qtd {qtdVotos} / cargo {codigoCargo} / tipo {tipoVoto} / partido {partido} / candidato {codigo}"
        identificacao = f"{codigo}{partido}"
    else:
        descricao = f"qtd {qtdVotos} / cargo {codigoCargo} / tipo {tipoVoto}"
        identificacao = ""

    claro = f"{codigoCargo}{tipoVoto}{qtdVotos}{identificacao}{carga}"
    claro = claro.encode("iso8859=1")
    hashed = hashlib.sha512(claro).digest()
    print(f"voto: {descricao}")
    try:
        verificador.verify(assinatura, hashed)
        print(f"assinatura OK {assinatura.hex()}")
    except:
        print(f"assinatura FALHOU {assinatura.hex()}")


def valida_assinatura_cargo(verificador: ed25519.VerifyingKey, carga: str, totalVotosCargo: dict):
    codigoCargo = totalVotosCargo["codigoCargo"][1]
    votosVotaveis = totalVotosCargo["votosVotaveis"]
    for votosVotavel in votosVotaveis:
        valida_assinatura_votavel(verificador, carga, codigoCargo, votosVotavel)


def valida_assainturas_votacao(verificador: ed25519.VerifyingKey, carga: str, resultadoVotacao: dict):
    totaisVotosCargo = resultadoVotacao["totaisVotosCargo"]
    for totalVotosCargo in totaisVotosCargo:
        valida_assinatura_cargo(verificador, carga, totalVotosCargo)


def valida_assinaturas_eleicao(verificador: ed25519.VerifyingKey, carga: str, resultadoPorEleicao: dict):
    resultadosVotacao = resultadoPorEleicao["resultadosVotacao"]
    for resultadoVotacao in resultadosVotacao:
        valida_assainturas_votacao(verificador, carga, resultadoVotacao)


def valida_assinaturas(bu: dict, verificador: ed25519.VerifyingKey):
    carga = bu["urna"]["correspondenciaResultado"]["carga"]["codigoCarga"]
    resultadosPorEleicao = bu["resultadosVotacaoPorEleicao"]
    for resultadoPorEleicao in resultadosPorEleicao:
        valida_assinaturas_eleicao(verificador, carga, resultadoPorEleicao)


def processa_bu(asn1_paths: list, bu_path: str):
    conv = asn1tools.compile_files(asn1_paths, numeric_enums=True)
    with open(bu_path, "rb") as bu:
        envelope_encoded = bytearray(bu.read())
    envelope_decoded = conv.decode("EntidadeEnvelopeGenerico", envelope_encoded)
    bu_encoded = envelope_decoded["conteudo"]
    bu_decoded = conv.decode("EntidadeBoletimUrna", bu_encoded)
    chave = bu_decoded["chaveAssinaturaVotosVotavel"]
    logging.debug("Chave de verificação: %s", chave.hex())
    verificador = ed25519.VerifyingKey(chave)

    valida_assinaturas(bu_decoded, verificador)


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

    logging.info("Verifica assinatura das tuplas do BU %s especificado em %s", bu_path, asn1_paths)
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
