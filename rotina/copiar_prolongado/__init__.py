from shutil import copy2
from os import path, makedirs
from datetime import datetime
from pytz import timezone

from escrita_logs import escrita_logs


def copiar_prolongado(log_email_exito, log_email_falha, bkp_data, dir_bkp, nome_arquivo, log_dir, dir_bkp_frio, servidor_banco, tipo_backup):
    
    dircompleto_bkp_frio = f'{dir_bkp_frio}/{servidor_banco}/{tipo_backup}'.replace('.', '_')
    nome_arquivo_log = f''
    
    if not path.isdir(dircompleto_bkp_frio):
        makedirs(dircompleto_bkp_frio)
    
    try:
        data_log_copiar = datetime.now(timezone("America/Sao_Paulo")).strftime("%Y/%m/%d %H:%M:%S.%f")
        copy2(f'{dir_bkp}/{nome_arquivo}', dircompleto_bkp_frio)
    except Exception as erro_copiar:
        nome_arquivo_log = f'{log_dir}/bakup_database_{bkp_data}__{servidor_banco}_stderr.log'
        mensagem_falha = f'\n[{data_log_copiar}] (-> Falha) Erro ao copiar arquivo {nome_arquivo} para Prolongado: ({erro_copiar})\n    {erro_copiar.with_traceback}'
        escrita_logs(log_email_exito, log_email_falha, nome_arquivo_log, mensagem_falha)
    else:
        nome_arquivo_log = f'{log_dir}/bakup_database_{bkp_data}__{servidor_banco}.log'
        mensagem_exito = f'\n[{data_log_copiar}] (Êxito ao copiar Prolongado) Arquivo {nome_arquivo} copiado com sucesso para Prolongado.'
        escrita_logs(log_email_exito, log_email_falha, nome_arquivo_log, mensagem_exito)
        