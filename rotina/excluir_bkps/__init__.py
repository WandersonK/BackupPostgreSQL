from os import path, remove, walk
from datetime import date, timedelta, datetime
from pytz import timezone

from escrita_logs import escrita_logs


tempo_delete_prolongado = date.today() - timedelta(60)  # Definir quantos dias para excluir os backups prolongados, atual 60 dias
tempo_delete_normal = date.today() - timedelta(30)  # Definir quantos dias para excluir os backups principais, atual 30 dias
data_log_excluir_frio = datetime.now(timezone("America/Sao_Paulo"))


def excluir(file_name, dir_completo, tempo_deletar, nome_arquivo_log, mensagem_exito, log_email_exito, log_email_falha):
    path_arquivo = path.join(dir_completo, file_name)
    vida_arquivo = date.fromtimestamp(path.getmtime(path_arquivo))
    
    if path.isfile(path_arquivo) and vida_arquivo < tempo_deletar:
        remove(path_arquivo)

        escrita_logs(log_email_exito, log_email_falha, nome_arquivo_log, mensagem_exito)


def excluir_bkps(dir_bkp, log_dir, log_email_exito, log_email_falha):
    for dir_completo, dir_name, file_names_list in walk(dir_bkp):
        for file_name in file_names_list:
            
            if 'BKP_PROLONGADO' in dir_completo:
                nome_arquivo_log = f'{log_dir}/excluir_backup_frio_{data_log_excluir_frio.strftime("%Y%m%d")}.log'
                mensagem_exito = f'\n[{data_log_excluir_frio.strftime("%Y/%m/%d %H:%M:%S.%f")}] (Êxito Excluir Backup Prolongado) Backup {file_name} em {dir_completo} completou mais de 60 dias e foi excluído com êxito!'
                excluir(file_name, dir_completo, tempo_delete_prolongado, nome_arquivo_log, mensagem_exito, log_email_exito, log_email_falha)
                
            elif 'log' not in dir_completo and 'BKP_PROLONGADO' not in dir_completo:
                nome_arquivo_log = f'{log_dir}/excluir_backup_{data_log_excluir_frio.strftime("%Y%m%d")}.log'
                mensagem_exito = f'\n[{data_log_excluir_frio.strftime("%Y/%m/%d %H:%M:%S.%f")}] (Êxito Excluir Backup Normal) Backup {file_name} em {dir_completo} completou mais de 30 dias e foi excluído com êxito!'
                excluir(file_name, dir_completo, tempo_delete_normal, nome_arquivo_log, mensagem_exito, log_email_exito, log_email_falha)
                