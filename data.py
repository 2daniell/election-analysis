from idlelib.iomenu import encoding

import pandas as pd
from datetime import datetime

dataFrame = pd.read_csv(
    'database/data.csv',
    encoding='latin1',
    delimiter=';')

def filter_nm_candidato(nm_candidato):
    results = dataFrame[dataFrame["NM_CANDIDATO"].str.contains(nm_candidato, case=False, na=False)]
    return results[['NR_CANDIDATO', 'NM_CANDIDATO', 'NM_URNA_CANDIDATO', "DS_CARGO", "NM_UE", 'NM_PARTIDO', 'SG_PARTIDO', 'SQ_CANDIDATO']]

def filter_nm_urna_candidato(nm_urna_candidato):
    results = dataFrame[dataFrame["NM_URNA_CANDIDATO"].str.contains(nm_urna_candidato, case=False, na=False)]
    return results[['NR_CANDIDATO', 'NM_CANDIDATO', 'NM_URNA_CANDIDATO', "DS_CARGO", "NM_UE", 'NM_PARTIDO', 'SG_PARTIDO', 'SQ_CANDIDATO']]

def filter_ds_cargo(ds_cargo):
    results = dataFrame[dataFrame["DS_CARGO"].str.contains(ds_cargo, case=False, na=False)]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

def filter_sg_partido(sg_partido):
    results = dataFrame[dataFrame["SG_PARTIDO"] == sg_partido]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

def filter_nm_partido(nm_partido):
    results = dataFrame[dataFrame["NM_PARTIDO"].str.contains(nm_partido, case=False, na=False)]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

def filter_nr_candidato(nr_candidato):
    results = dataFrame[dataFrame["NR_CANDIDATO"] == nr_candidato]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

def filter_nm_ue(nm_ue):
    results = dataFrame[dataFrame["NM_UE"].str.contains(nm_ue, case=False, na=False)]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

def filter_sq_candidato(sq_candidato):
    results = dataFrame[dataFrame["SQ_CANDIDATO"] == sq_candidato]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

def results_initial(number):
    return dataFrame.head(number)[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

#Procurar SQ_UE
def municipio_results():
    return dataFrame[["NM_UE", "SQ_UE"]].drop_duplicates().reset_index(drop=True)


redesFrame = pd.read_csv('database/redes.csv',
                         encoding='latin1',
                         delimiter=';')

def filter_media_sq_candidato(sq_candidato):
    results = redesFrame[redesFrame["SQ_CANDIDATO"] == sq_candidato]
    return results[['DS_URL']]

bensFrame = pd.read_csv('database/bens.csv',
                        encoding='latin1',
                        delimiter=';')


def find_bens_value(sq_candidato):
    result = bensFrame[bensFrame['SQ_CANDIDATO'] == sq_candidato].copy()

    if (result.empty):
        return 0.0

    result['VR_BEM_CANDIDATO'] = result['VR_BEM_CANDIDATO'].str.replace(',', '.')
    total = result['VR_BEM_CANDIDATO'].astype(float).sum()

    return float(total)


def get_statistics():
    cargos = dataFrame['DS_CARGO'].unique()
    result = []

    for cargo in cargos:
        candidatos = dataFrame[dataFrame['DS_CARGO'] == cargo].copy()

        total_candidatos = candidatos.shape[0]

        total_fem_candidates = candidatos[candidatos['DS_GENERO'] == 'FEMININO'].shape[0]
        total_masc_candidates = candidatos[candidatos['DS_GENERO'] == 'MASCULINO'].shape[0]

        porcent_fem = (total_fem_candidates / total_candidatos * 100) if total_candidatos > 0 else 0
        porcent_masc = (total_masc_candidates / total_candidatos * 100) if total_candidatos > 0 else 0

        graus_instrucao = candidatos['DS_GRAU_INSTRUCAO'].unique()
        porcentagem_instrucao = {}

        for grau in graus_instrucao:
            total_por_grau = candidatos[candidatos['DS_GRAU_INSTRUCAO'] == grau].shape[0]
            porcent_grau = (total_por_grau / total_candidatos * 100) if total_candidatos > 0 else 0
            porcentagem_instrucao[grau] = int(porcent_grau)

        candidatos['IDADE'] = pd.to_datetime(candidatos['DT_NASCIMENTO'], format='%d/%m/%Y').apply(
            lambda x: datetime.today().year - x.year - (
                        (datetime.today().month, datetime.today().day) < (x.month, x.day)))

        faixa_21 = candidatos[candidatos['IDADE'] <= 21].shape[0]
        faixa_22_40 = candidatos[(candidatos['IDADE'] >= 22) & (candidatos['IDADE'] <= 40)].shape[0]
        faixa_41_60 = candidatos[(candidatos['IDADE'] >= 41) & (candidatos['IDADE'] <= 60)].shape[0]
        faixa_60 = candidatos[candidatos['IDADE'] > 60].shape[0]

        porcent_faixas = {
            'faixa_21': int(faixa_21),
            'faixa_22_40': int(faixa_22_40),
            'faixa_41_60': int(faixa_41_60),
            'faixa_60': int(faixa_60),
        }

        estados_civis = candidatos['DS_ESTADO_CIVIL'].unique()
        porcentagem_estado_civil = {}

        for estado in estados_civis:
            total_por_estado = candidatos[candidatos['DS_ESTADO_CIVIL'] == estado].shape[0]
            porcent_estado = (total_por_estado / total_candidatos * 100) if total_candidatos > 0 else 0
            porcentagem_estado_civil[estado] = int(porcent_estado)

        result.append({
            'cargo': cargo,
            'total_candidatos': total_candidatos,
            'porcent_fem': int(porcent_fem),
            'porcent_masc': int(porcent_masc),
            'porcent_instrucao': porcentagem_instrucao,
            'idd_faixas': porcent_faixas,
            'porcentagem_estado_civil': porcentagem_estado_civil
        })

    return result


def get_partidos_prefeito():
    candidatos_prefeito = dataFrame[dataFrame['DS_CARGO'] == 'PREFEITO']
    partidos_prefeito = candidatos_prefeito['SG_PARTIDO'].unique()
    return partidos_prefeito.tolist()


