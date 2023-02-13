from threading import Thread
import subprocess
from pytz import timezone
from datetime import datetime

from gerar_dump import gerar_dump
from escrita_logs import escrita_logs


def bancos_listagem(log_email_exito, log_email_falha, bkp_data, log_dir, tipo_backup, dir_bkp_destino, dir_bkp_frio, servidor_banco, porta_banco=5431):
    lista_bancos = ['psql', '-U', 'ubkp_apl', '-h', f'{servidor_banco}', '-p', f'{porta_banco}', '-d', 'postgres', '-t', '-c', 'SELECT datname from pg_database WHERE datname not in (\'template0\', \'template1\', \'postgres\') order by 1']
    lista_bancos = subprocess.run(lista_bancos, capture_output=True)

    if lista_bancos.returncode != 0:
        data_log_listarbancos = datetime.now(timezone("America/Sao_Paulo")).strftime('%Y/%m/%d %H:%M:%S.%f')
        mensagem_falha = f"\n[{data_log_listarbancos}] (-> Falha Listagem Bancos {servidor_banco}): {lista_bancos.stderr}"
        nome_arquivo_log = f'{log_dir}/bakup_database_{bkp_data}__{servidor_banco}_stderr.log'.replace('.', '_')
        escrita_logs(log_email_exito, log_email_falha, nome_arquivo_log, mensagem_falha)
        
    lista_bancos = (lista_bancos.stdout.decode()).split()
    
    Thread(target=gerar_dump, args=(lista_bancos, log_email_exito, log_email_falha, tipo_backup, dir_bkp_destino, bkp_data, log_dir, dir_bkp_frio, servidor_banco, porta_banco)).start()
