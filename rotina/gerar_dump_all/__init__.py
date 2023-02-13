import subprocess
from os import path, makedirs
from datetime import datetime
from pytz import timezone

from escrita_logs import escrita_logs
from copiar_prolongado import copiar_prolongado


def gerar_dump_all(log_email_exito, log_email_falha, tipo_backup, log_dir, dir_bkp_destino, bkp_data, dir_bkp_frio, servidor_banco, porta_banco=5431):
    from threading import Thread
    
    nome_arquivo = f'BKP_{bkp_data}_ALL.sql'
    # dir_bkp = f'{dir_bkp_destino}/{str(porta_banco)}'
    dir_bkp = f'{dir_bkp_destino}/{servidor_banco}/{tipo_backup}'.replace('.', '_')
    
    if not path.isdir(dir_bkp):
        makedirs(dir_bkp)
    
    comando_preparo = ['pg_dumpall', '-U', 'ubkp_apl', '-h', f'{servidor_banco}', '-p', f'{porta_banco}', '-f', f'{dir_bkp}/{nome_arquivo}']
    saida_dump = subprocess.run(comando_preparo, capture_output=True, text=True)
    data_termino = datetime.now(timezone("America/Sao_Paulo")).strftime("%Y/%m/%d %H:%M:%S.%f")

    # 'returncode = 0' executado com êxito.
    if saida_dump.returncode == 0:
        nome_arquivo_log = f'{log_dir}/bakup_database_{bkp_data}__{servidor_banco}.log'
        mensagem_exito = f'\n[{data_termino}] (Êxito no pg_dumpall) Backup do Database: {servidor_banco}'
        escrita_logs(log_email_exito, log_email_falha, nome_arquivo_log, mensagem_exito)
    else:
        nome_arquivo_log = f'{log_dir}/bakup_database_{bkp_data}__{servidor_banco}_stderr.log'
        mensagem_falha = f'\n[{data_termino}] (-> Falha no pg_dumpall) Backup do Database {servidor_banco}: {saida_dump.stderr}'
        escrita_logs(log_email_exito, log_email_falha, nome_arquivo_log, mensagem_falha)
    
    # global th
    
    Thread(target=compactar_dumps, args=(log_email_exito, log_email_falha, tipo_backup, bkp_data, log_dir, dir_bkp, nome_arquivo, dir_bkp_frio, servidor_banco)).start()
    

def compactar_dumps(log_email_exito, log_email_falha, tipo_backup, bkp_data, log_dir, dir_bkp, nome_arquivo, dir_bkp_frio, servidor_banco):
    
    from shutil import make_archive, Error
    # Compacta o arquivo de backup e grava log se erro
    excluir_pos_compactado = True
    
    try:
        make_archive(f'{dir_bkp}/{nome_arquivo}', 'gztar', f'{dir_bkp}/', nome_arquivo)
        copiar_prolongado(log_email_exito, log_email_falha, bkp_data, dir_bkp, nome_arquivo, log_dir, dir_bkp_frio, servidor_banco, tipo_backup)
    except (Exception, Error) as erro_comp:
        data_log_comp = datetime.now(timezone("America/Sao_Paulo")).strftime("%Y/%m/%d %H:%M:%S.%f")
        nome_arquivo_log = f'{log_dir}/bakup_database_{bkp_data}__{servidor_banco}_stderr.log'
        mensagem_falha = f'\n[{data_log_comp}] (-> Falha) Erro na compactação do arquivo {nome_arquivo}: ({erro_comp})\n    {erro_comp.with_traceback}'
        escrita_logs(log_email_exito, log_email_falha, nome_arquivo_log, mensagem_falha)
        excluir_pos_compactado = False
        
    excluir_dump_pos_compactado(log_email_exito, log_email_falha, bkp_data, log_dir, dir_bkp, nome_arquivo, servidor_banco, excluir_pos_compactado)
    

def excluir_dump_pos_compactado(log_email_exito, log_email_falha, bkp_data, log_dir, dir_bkp, nome_arquivo, servidor_banco, excluir_pos_compactado):
    # Excluir o arquivo sql, se compactação finalizar em êxito
    if excluir_pos_compactado:
        excluir_comando = ['rm', f'{dir_bkp}/{nome_arquivo}']
        resultado_excluir = subprocess.run(excluir_comando, capture_output=True, text=True)
        data_log_excluir = datetime.now(timezone("America/Sao_Paulo")).strftime('%Y/%m/%d %H:%M:%S.%f')
        nome_arquivo_log = f'{log_dir}/bakup_database_{bkp_data}__{servidor_banco}.log'
        
        if resultado_excluir.returncode == 0:
            mensagem_exito = f'\n[{data_log_excluir}] (Êxito) Arquivo {nome_arquivo} excluído e compactado com sucesso.'
            escrita_logs(log_email_exito, log_email_falha, nome_arquivo_log, mensagem_exito)
        else:
            mensagem_falha = f'\n[{data_log_excluir}] (-> Falha) Erro ao excluir arquivo {nome_arquivo}: {resultado_excluir.stderr}'
            escrita_logs(log_email_exito, log_email_falha, nome_arquivo_log, mensagem_falha)
        