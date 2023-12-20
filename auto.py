import pandas as pd
import smtplib
import email.message

# importar a base de dados
tabela_vendas = pd.read_excel('Vendas.xlsx')
print(tabela_vendas)
print('='*50)

# visualizar a base de dados sem ocultar nenhuma coluna
pd.set_option('display.max_columns', None)

# faturamento por loja
faturamento = tabela_vendas[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
print(faturamento)
print('='*50)

# quantidade de produtos vendidos por loja
quantidade = tabela_vendas[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
print(quantidade)
print('='*50)

# ticket médio por produto de cada loja
ticket_medio = (faturamento['Valor Final'] / quantidade['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0: 'Ticket médio'})
print(ticket_medio)


# enviar um email com o relatório
def enviar_email():
    corpo_email = f'''
    <p>Prezados,</p>
    
    <p>Segue o relatório de vendas por loja.</p>
    
    <p>Faturamento:</p>
    {faturamento.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})}
    <br>
    <p>Quantidade vendido por loja:</p>
    {quantidade.to_html(formatters={'Valor Final': 'R${:,}'.format})}
    <br>
    <p>Ticket médio dos produtos em cada loja:</p>
    {ticket_medio.to_html(formatters={'Ticket médio': 'R${:,.2f}'.format})}
    <br>
    <p>Qualquer dúvida estou à disposição.</p>
    
    <p>Att.,</p>
    <p>Adélia</p>
    '''

    msg = email.message.Message()
    msg['Subject'] = 'Relatório de vendas por loja'
    msg['From'] = 'remetente'
    msg['To'] = 'destinatário'
    password = 'senha'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado!')


enviar_email()
