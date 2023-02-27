
def notificar_email(servidor_banco, dir_bkp_destino, pasta_rotina, tipo_backup, log_email_exito, log_email_falha, user_email, pass_email):
    
    from hurry.filesize import size, si
    from shutil import disk_usage
    from smtplib import SMTP_SSL
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    log_email_falha_formatado = ''
    log_email_exito_formatado = ''
    
    disk = disk_usage(dir_bkp_destino)
    total_disk = size(disk.total, system=si)
    used_disck = size(disk.used, system=si)
    free_disk = size(disk.free, system=si)

    emails_lista = open(f'{pasta_rotina}/contatos_to.txt').read().split()
    
    # Preparando corpo de Êxito e Falha
    for log_email_falha_individual in log_email_falha:
        log_email_falha_formatado += f'<li style="margin-left:15px">{log_email_falha_individual}</li>'
    
    for log_email_exito_individual in log_email_exito:
        log_email_exito_formatado += f'<li style="margin-left:15px">{log_email_exito_individual}</li>'
    
    mensagem_template = f"""
<div>
    <div>
        <b>Servidor:</b>&nbsp;{servidor_banco}
        <div><b>Status do backup:</b></div>
        <div><b>Êxito</b></div>
        <div>
            <ul>
                {log_email_exito_formatado}
            </ul>
        </div>
        <div><b>Falhas</b></div>
        <div>
            <ul>
                {log_email_falha_formatado}
            </ul>
        </div>
        <div><b>Status do disco:</b></div>
        <div>
            <ul>
                <li style="margin-left:15px"><b>Total:&nbsp;</b>{total_disk}</li>
                <li style="margin-left:15px"><b>Em Uso:&nbsp;</b>{used_disck}<b>&nbsp;</b></li>
                <li style="margin-left:15px"><b>Livre:&nbsp;</b>{free_disk}</li>
            </ul>
            <div><font color="#ffffff" style="font-size: 1px;">ZDpB4Ife2LAEEwmMlJDQ</font></div>
        </div>
    </div>
</div>
    """
    
    conexao_smtp = SMTP_SSL('smtp.gmail.com', 465)
    conexao_smtp.login(user_email, pass_email)
    
    infos_mensagem = MIMEMultipart('alternative')
    infos_mensagem['From'] = user_email
    infos_mensagem['To'] = user_email
    infos_mensagem['Subject'] = f'Rotina {tipo_backup} Backup Banco de Dados {servidor_banco}'
    infos_mensagem.attach(MIMEText(mensagem_template, 'html'))
    
    conexao_smtp.sendmail(user_email, emails_lista, infos_mensagem.as_string())
    conexao_smtp.quit()
