from escrita_logs import escrita_logs
from copiar_prolongado import copiar_prolongado


def gerar_dump(lista_bancos, log_email_exito, log_email_falha, tipo_backup, dir_bkp_destino, bkp_data, log_dir, dir_bkp_frio, servidor_banco, porta_banco):
    from os import makedirs, path
    import subprocess
    from datetime import datetime
    from pytz import timezone
    
    for db in lista_bancos:
        dir_bkp = f'{dir_bkp_destino}/{servidor_banco}/{tipo_backup}'.replace('.', '_')
        
        if not path.isdir(dir_bkp):
            makedirs(dir_bkp)
        
        if tipo_backup == 'DIARIO':
            nome_arquivo = f'BKP_{db}_{bkp_data}.compressed'
            comando_preparo = ['pg_dump', '-U', 'ubkp_apl', '-h', f'{servidor_banco}', '-p', f'{porta_banco}', '-Z', '9', '-d', f'{db}', '-N', 'stage', '-N', 'audit', '-f', f'{dir_bkp}/{nome_arquivo}']
        elif tipo_backup == 'SEMANAL':
            nome_arquivo = f'BKP_{db}_STAGE_AUDIT_{bkp_data}.compressed'
            comando_preparo = ['pg_dump', '-U', 'ubkp_apl', '-h', f'{servidor_banco}', '-p', f'{porta_banco}', '-Z', '9', '-d', f'{db}', '-f', f'{dir_bkp}/{nome_arquivo}']
        
        
        saida_dump = subprocess.run(comando_preparo, capture_output=True, text=True)
        data_termino = datetime.now(timezone("America/Sao_Paulo")).strftime("%Y/%m/%d %H:%M:%S.%f")

        copiar_prolongado(log_email_exito, log_email_falha, bkp_data, dir_bkp, nome_arquivo, log_dir, dir_bkp_frio, servidor_banco, tipo_backup)
        
        # 'returncode = 0' executado com êxito.
        if saida_dump.returncode == 0:
            nome_arquivo_log = f'{log_dir}/bakup_database_{bkp_data}__{servidor_banco}.log'
            mensagem_exito = f'\n[{data_termino}] (Êxito no pg_dump) Backup do Database: {db}'
            escrita_logs(log_email_exito, log_email_falha, nome_arquivo_log, mensagem_exito)
        else:
            nome_arquivo_log = f'{log_dir}/bakup_database_{bkp_data}__{servidor_banco}_stderr.log'
            mensagem_falha = f'\n[{data_termino}] (-> Falha no pg_dump) Backup do Database {db}: {saida_dump.stderr}'
            escrita_logs(log_email_exito, log_email_falha, nome_arquivo_log, mensagem_falha)
        