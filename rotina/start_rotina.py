#!/bin/python3

from threading import enumerate
from sys import argv
from datetime import datetime
from pytz import timezone
from os import path, makedirs

from gerar_dump_all import gerar_dump_all
from bancos_listagem import bancos_listagem
from notificar_email import notificar_email
from excluir_bkp_frio import excluir_bkp_frio


pasta_rotina = '/home/ubkp/rotina' # Utilizado pela def email e variavel servidores_files
dir_bkp_destino = '/bkpcomp' # Utilizado pela def gerar_dump e email
dir_bkp_frio = '/bkpcomp/BKP_PROLONGADO'
bkp_data = datetime.now(timezone("America/Sao_Paulo")).strftime('%Y%m%d')
log_dir = '/bkpcomp/log'
servidores_file = open(f'{pasta_rotina}/servidores_bd.txt')
user_email = 'ENDEREÇO DE EMAIL AQUI'
pass_email = 'SENHA DO EMAIL AQUI'
tipo_backup = argv[1].upper() # DIARIO, SEMANAL, MENSAL
user_banco = 'backup'

if not path.isdir(log_dir):
    makedirs(log_dir)


for server_e_porta in servidores_file:
    
    log_email_falha = []
    log_email_exito = []
    
    if len(server_e_porta.split()) > 1:
        servidor_banco = server_e_porta.split()[0]
        portas_lista = server_e_porta.split()[1:]
        
        for porta in portas_lista:
            if tipo_backup == 'MENSAL':
                gerar_dump_all(log_email_exito, log_email_falha, tipo_backup, log_dir, dir_bkp_destino, bkp_data, dir_bkp_frio, user_banco, servidor_banco, porta)
            else:
                bancos_listagem(log_email_exito, log_email_falha, bkp_data, log_dir, tipo_backup, dir_bkp_destino, dir_bkp_frio, user_banco, servidor_banco, porta)
            
    else:
        servidor_banco = server_e_porta.split()[0]
        if tipo_backup == 'MENSAL':
            gerar_dump_all(log_email_exito, log_email_falha, tipo_backup, log_dir, dir_bkp_destino, bkp_data, dir_bkp_frio, user_banco, servidor_banco)
        else:
            bancos_listagem(log_email_exito, log_email_falha, bkp_data, log_dir, tipo_backup, dir_bkp_destino, dir_bkp_frio, user_banco, servidor_banco)

    threads = enumerate()
    for thread in threads[1:]:
        thread.join()
    
    excluir_bkp_frio(dir_bkp_frio, log_dir, log_email_exito, log_email_falha)
    
    notificar_email(servidor_banco, dir_bkp_destino, pasta_rotina, tipo_backup, log_email_exito, log_email_falha, user_email, pass_email)
    
    
servidores_file.close()
