# Rotina de Backup PostgreSQL

## CONFIGURAÇÕES GERAIS
Na pasta onde estarão os arquivos da rotina, existem dois arquivos de texto que necessitam de preenchimento manual, são:

* servidores_bd.txt
* contatos_to.txt
* start_rotina.py

No "servidores_bd.txt", ficam os servidores seguido das portas caso necessário, cada servidor com porta, separados em linha, a estrutura é a seguinte: \<IP/SERVIDOR\> \<PORTA\> \<PORTA\>

Exemplo:

* 255.255.0.25 5432
* 255.255.0.26
* 255.255.0.27 5433 5432 5431
* 255.255.0.28

Se não for especificado uma porta, a padrão utilizada será a **5431**. Várias portas podem ser especificadas, separadas por espaço, na mesma linha do servidor, conforme o exemplo.

No "contatos_to.txt", ficam os e-mails para os quais serão enviadas as notificações. Basta preencher por linha com o endereço de e-mail.

Exemplo:

* destinatario.1@topocart.com.br
* destinatario.2@topocart.com.br
* destinatario.3@topocart.com.br

No "start_rotina.py", só é necessário preenchimento caso altere a estrutura das pastas, usuário ou senha de e-mail. Essas informações ficam nas primeiras linhas do script.

Uma especificação das variáveis:

* **pasta_rotina:** é onde ficam os arquivos do script, no usuário ubkp. Por padrão, está como /home/ubkp/rotina
* **dir_bkp_destino:** é o compartilhamento do storage, onde ficam os arquivos backupeados. Por padrão, está como /bkpcomp
* **log_dir:** é a pasta onde ficaram os logs, sendo realizado por backup feito e servidor. Será um arquivo por dia, semana e mês feito. Por padrão, está como /bkpcomp/log
* **user_email:** é o e-mail pelo qual serão enviadas as notificações.
* **pass_email:** é a senha do e-mail.
* **user_banco:** é o usuário do seu banco de dados. É recomendável utilizar um usuário padrão nos bancos com acesso restrito apenas a backup. Assim facilita a configuração no script de rotina.

## OUTRAS CONFIGURAÇÕES
### Dias para excluir arquivos da pasta prolongado
O tempo definido para excluir os arquivos do Prolongado, são de 60 dias, caso seja necessário alterar, deve-se acessar o pacote "excluir_bkps". Lá haverá uma variável chamada "tempo_delete_prolongado", entre parênteses na função "timedelta", informe o tempo desejado.

O mesmo vale para o tempo do backup principal, que contém a variável "tempo_delete_normal", que atualmente está definido para 30 dias.

Na mensagem para o log, o dia está sendo descrito, altere também conforme o dia escolhido, na variável "mensagem_exito".

### Bancos desconsiderados no DIARIO
Alguns bancos foram desconsiderados do backup diário, caso seja necessário adicionar ou remover algum, deve-se editar o pacote "gerar_dump", na variável "comando_preparo", onde contém o parâmetro -N. Para adicionar um novo, informe com a mesma estrutura, respeitando as aspas e vírgulas.
