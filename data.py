import pandas as pd

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

def results_initial(number):
    return dataFrame.head(number)[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]
