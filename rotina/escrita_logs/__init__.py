
def escrita_logs(log_email_exito, log_email_falha, nome_elocal_arquivo, mensagem_gravar):
    
    # nome_elocal_arquivo = str(nome_elocal_arquivo).replace('.', '_')
    
    arquivo_log = open(nome_elocal_arquivo, 'a', encoding='UTF-8')  # O 'a' indica append, insere linha seguida, sem sobrepor o existente
    arquivo_log.write(mensagem_gravar)
    arquivo_log.close()
    
    if '-> Falha' in mensagem_gravar:
        log_email_falha.append(mensagem_gravar)
    else:
        log_email_exito.append(mensagem_gravar)
    