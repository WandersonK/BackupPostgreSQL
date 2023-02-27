from os import path, remove, walk
from datetime import date, timedelta, datetime
from pytz import timezone

from escrita_logs import escrita_logs


tempo_delete = date.today() - timedelta(60)  # Definir quantos dias para excluir os backups, atual 60 dias
data_log_excluir_frio = datetime.now(timezone("America/Sao_Paulo"))

def excluir_bkp_frio(dir_bkp_frio, log_dir, log_email_exito, log_email_falha):
    for dir_completo, dir_name, file_names_list in walk(dir_bkp_frio):

        for file_name in file_names_list:
            path_arquivo = path.join(dir_completo, file_name)
            vida_arquivo = date.fromtimestamp(path.getmtime(path_arquivo))
            
            if path.isfile(path_arquivo) and vida_arquivo < tempo_delete:
                remove(path_arquivo)

                nome_arquivo_log = f'{log_dir}/excluir_backup_frio_{data_log_excluir_frio.strftime("%Y%m%d")}.log'
                mensagem_exito = f'\n[{data_log_excluir_frio.strftime("%Y/%m/%d %H:%M:%S.%f")}] (Êxito Excluir Backup Prolongado) Backup {file_name} em {dir_completo} completou mais de 60 dias e foi excluído com êxito!'
                escrita_logs(log_email_exito, log_email_falha, nome_arquivo_log, mensagem_exito)
    