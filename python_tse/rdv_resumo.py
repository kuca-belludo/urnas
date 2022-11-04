import argparse
import logging
import os
import sys

import asn1crypto.core as asn1


class CargoConstitucional(asn1.Enumerated):
    _map = {
        1:  "Presidente",
        2:  "Vice Presidente",
        3:  "Governador",
        4:  "Vice Governador",
        5:  "Senador",
        6:  "Deputado Federal",
        7:  "Deputado Estadual",
        8:  "Deputado Distrital",
        9:  "Primeiro SuplenteSenador",
        10: "Segundo SuplenteSenador",
        11: "Prefeito",
        12: "Vice Prefeito",
        13: "Vereador",
    }


class Fase(asn1.Enumerated):
    _map = {
        1: "simulado",
        2: "oficial",
        3: "treinamento",
    }


class MotivoApuracaoEletronica(asn1.Enumerated):
    _map = {
        1:  "naoFoiPossivelReuperarResultado",
        2:  "urnaNaoChegouMidiaDefeituosa",
        3:  "urnaNaoChegouMidiaExtraviada",
        99: "outros",
    }


class MotivoApuracaoManual(asn1.Enumerated):
    _map = {
        1:  "urnaComDefeito",
        2:  "urnaIndisponivelInicio",
        3:  "urnaOutraSecao",
        99: "outros",
    }


class MotivoApuracaoMistaComBU(asn1.Enumerated):
    _map = {
        1:  "urnaDataHoraIncorreta",
        2:  "urnaComDefeito",
        3:  "urnaOutrasecao",
        4:  "urnaPreparadaIncorretamente",
        5:  "urnaChegouAposInicioVotacao",
        99: "outros",
    }


class MotivoApuracaoMistaComMR(asn1.Enumerated):
    _map = {
        1:  "naoObteveExitoContingencia",
        2:  "indisponibilidadeUrnaContingencia",
        3:  "indisponibilidadeFlashContingencia",
        4:  "problemaEnergiaEletrica",
        5:  "naoFoiPossivelTrocarUrna",
        6:  "naoFoiSolicitadaTrocaUrna",
        99: "outros",
    }


class OrigemVotosSA(asn1.Enumerated):
    _map = {
        1: "cedula",
        2: "rdv",
        3: "bu",
    }


class TipoApuracao(asn1.Enumerated):
    _map = {
        1: "totalmenteManual",
        2: "totalmenteEletronica",
        3: "mistaBU",
        4: "mistaMR",
    }


class TipoArquivo(asn1.Enumerated):
    _map = {
        1: "votacaoUE",
        2: "votacaoRED",
        3: "saMistaMRParcialCedula",
        4: "saMistaBUImpressoCedula",
        5: "saManual",
        6: "saEletronica",
    }


class TipoCedulaSA(asn1.Enumerated):
    _map = {
        1: "majoritario",
        2: "proporcional",
    }


class TipoUrna(asn1.Enumerated):
    _map = {
        1: "secao",
        3: "contingencia",
        4: "reservaSecao",
        6: "reservaEncerrandoSecao",
    }


class TipoVoto(asn1.Enumerated):
    _map = {
        1: "legenda",
        2: "nominal",
        3: "branco",
        4: "nulo",
        5: "brancoAposSuspensao",
        6: "nuloAposSuspensao",
        7: "nuloPorRepeticao",
        8: "nuloCargoSemCandidato",
        9: "nuloAposSuspensaoCargoSemCandidato",
    }


class MunicipioZona(asn1.Sequence):
    _fields = [
        ("municipio",   asn1.Integer),
        ("zona",        asn1.Integer),
    ]


class IdentificacaoContingencia(asn1.Sequence):
    _fields = [
        ("municipioZona", MunicipioZona),
    ]


class IdentificacaoSecaoEleitoral(asn1.Sequence):
    _fields = [
        ("municipioZona",   MunicipioZona),
        ("local",           asn1.Integer),
        ("secao",           asn1.Integer),
    ]


class IdentificacaoUrna(asn1.Choice):
    _alternatives = [
        ("identificacaoSecaoEleitoral", IdentificacaoSecaoEleitoral,    {"implicit": 0}),
        ("identificacaoContingencia",   IdentificacaoContingencia,      {"implicit": 1}),
    ]


class Carga(asn1.Sequence):
    _fields = [
        ("numeroInternoUrna",   asn1.Integer),
        ("numeroSerieFC",       asn1.OctetString),
        ("dataHoraCarga",       asn1.GeneralString),
        ("codigoCarga",         asn1.GeneralString),
    ]


class CorrespondenciaResultado(asn1.Sequence):
    _fields = [
        ("identificacao",   IdentificacaoUrna),
        ("carga",           Carga),
    ]


class ApuracaoEletronica(asn1.Sequence):
    _fields = [
        ("tipoapuracao",    TipoApuracao),
        ("motivoApuracao",  MotivoApuracaoEletronica),
    ]


class ApuracaoMistaBUAE(asn1.Sequence):
    _fields = [
        ("tipoapuracao",    TipoApuracao),
        ("motivoApuracao",  MotivoApuracaoMistaComBU),
    ]


class ApuracaoMistaMR(asn1.Sequence):
    _fields = [
        ("tipoApuracao",    TipoApuracao),
        ("motivoApuracao",  MotivoApuracaoMistaComMR),
    ]


class ApuracaoTotalmenteManualDigitacaoAE(asn1.Sequence):
    _fields = [
        ("tipoapuracao",    TipoApuracao),
        ("motivoApuracao",  MotivoApuracaoManual),
    ]


class IDEleitoral(asn1.Choice):
    _alternatives = [
        ("idProcessoEleitoral", asn1.Integer, {"implicit": 1}),
        ("idPleito",            asn1.Integer, {"implicit": 2}),
        ("idEleicao",           asn1.Integer, {"implicit": 3}),
    ]


class TipoApuracaoSA(asn1.Choice):
    _alternatives = [
        ("apuracaoMistaMR",             ApuracaoMistaMR,                        {"implicit": 0}),
        ("apuracaoMistaBUAE",           ApuracaoMistaBUAE,                      {"implicit": 1}),
        ("apuracaoTotalmenteManual",    ApuracaoTotalmenteManualDigitacaoAE,    {"implicit": 2}),
        ("apuracaoEletronica",          ApuracaoEletronica,                     {"implicit": 3}),
    ]


class CabecalhoEntidade(asn1.Sequence):
    _fields = [
        ("dataGeracao", asn1.GeneralString),
        ("idEleitoral", IDEleitoral)
    ]


class Urna(asn1.Sequence):
    _fields = [
        ("tipoUrna",                    TipoUrna),
        ("versaoVotacao",               asn1.GeneralString),
        ("correspondenciaResultado",    CorrespondenciaResultado),
        ("tipoArquivo",                 TipoArquivo),
        ("numeroSerieFV",               asn1.OctetString),
        ("motivoUtilizacaoSA",          TipoApuracaoSA, {"optional": True}),
    ]


class Voto(asn1.Sequence):
    _fields = [
        ("tipoVoto",    TipoVoto),
        ("digitacao",   asn1.NumericString, {"optional": True}),
    ]


class SequenceOfVotos(asn1.SequenceOf):
    _child_spec = Voto


class CodigoCargoConsulta(asn1.Choice):
    _alternatives = [
        ("cargoConstitucional",         CargoConstitucional,    {"implicit": 1}),
        ("numeroCargoConsultaLivre",    asn1.Integer,           {"implicit": 2}),
    ]


class VotosCargo(asn1.Sequence):
    _fields = [
        ("idCargo",             CodigoCargoConsulta),
        ("quantidadeEscolhas",  asn1.Integer),
        ("votos",               SequenceOfVotos),
    ]


class SequenceOfVotosCargo(asn1.SequenceOf):
    _child_spec = VotosCargo


class EleicaoVota(asn1.Sequence):
    _fields = [
        ("idEleicao",   asn1.Integer),
        ("votosCargos", SequenceOfVotosCargo),
    ]


class EleicaoSA(asn1.Sequence):
    _fields = [
        ("idEleicao",       asn1.Integer),
        ("tipoCedulaSA",    TipoCedulaSA),
        ("origemVotosSA",   OrigemVotosSA),
        ("votosCargos",     SequenceOfVotosCargo),
    ]


class SequenceOfEleicaoVota(asn1.SequenceOf):
    _child_spec = EleicaoVota


class SequenceOfEleicaoSA(asn1.SequenceOf):
    _child_spec = EleicaoSA


class Eleicoes(asn1.Choice):
    _alternatives = [
        ("eleicoesVota",    SequenceOfEleicaoVota,  {"implicit": 0}),
        ("eleicoesSA",      SequenceOfEleicaoSA,    {"implicit": 1}),
    ]


class EntidadeRegistroDigitalVoto(asn1.Sequence):
    _fields = [
        ("pleito",          asn1.Integer),
        ("fase",            Fase),
        ("identificacao",   IdentificacaoSecaoEleitoral),
        ("eleicoes",        Eleicoes),
    ]


class EntidadeResultadoRDV(asn1.Sequence):
    _fields = [
        ("cabecalho",   CabecalhoEntidade),
        ("urna",        Urna),
        ("rdv",         EntidadeRegistroDigitalVoto),
    ]


def imprime_rdv(rdv_path: str):
    logging.debug("Lendo arquivo %s", rdv_path)
    with open(rdv_path, "rb") as file:
        encoded_rdv = file.read()
    resultado_rdv = EntidadeResultadoRDV.load(encoded_rdv)
    rdv = resultado_rdv["rdv"]
    eleicoes = rdv["eleicoes"].chosen
    print("=" * 40)
    for eleicao in eleicoes:
        votos_cargos = eleicao["votosCargos"]
        for votos_cargo in votos_cargos:
            qtd = 0
            print("-" * 40)
            print(f"{votos_cargo['idCargo'].chosen.native}")
            votos = votos_cargo["votos"]
            for voto in votos:
                qtd += 1
                digitacao = voto["digitacao"]
                tipo = voto["tipoVoto"]
                if digitacao == asn1.VOID:
                    print(f"{qtd:3} - {tipo.native}")
                else:
                    print(f"{qtd:3} - {tipo.native:8} - [{digitacao}]")
    print("=" * 40)


def main():
    parser = argparse.ArgumentParser(
        description="Lê um Registro Digital do Voto (RDV) da Urna Eletrônica (UE) e imprime seu conteúdo",
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-r", "--rdv", type=str, required=True,
                        help="Caminho para o arquivo de RDV originado na UE")
    parser.add_argument("--debug", action="store_true", help="ativa o modo DEBUG do log")

    args = parser.parse_args()

    rdv_path = args.rdv
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info("Converte RDV %s", rdv_path)
    if not os.path.exists(rdv_path):
        logging.error("Arquivo do RDV (%s) não encontrado", rdv_path)
        sys.exit(-1)

    imprime_rdv(rdv_path)


if __name__ == "__main__":
    main()
