#!/usr/bin/env python
# coding: utf-8

# In[98]:


# Configurações para a apresentação de slides com o Jupyter Notebook
# Instalar temas do Jupyter:
# >> pip install jupyterthemes
# Listar temas disponíveis:
# >> jt -l
# Selecionar o tema para a apresentação:
# >> jt -t monokai
# Retornar ao tema original:
# >> jt -r

from notebook.services.config import ConfigManager
cm = ConfigManager()
cm.update('livereveal', {
    "start_slideshow_at": "selected",
    "transition": "zoom",
    "height": 768,
    "width": 1024,
    "theme": "simple",
    "scroll": True,
})


# # EPM Web API (Python) - primeiros passos...

# ## Operações típicas
# 
# 1. **Estabelecimento de Conexão** (=sessão) com um **EPM Server** (=servidor de dados)
# 2. **Criação** das variáveis de interesse
#     * definir variáveis de interesse (eventualmente suas propriedades)
#     * executar criação no ambiente Python da variável de interesse (contraparte do **EPM Server**)
# 3. **Leitura** de valores escalares
#     * definir variável de interesse
#     * executar leitura
# 4. **Leitura** de valores históricos
#     * definir variável de interesse
#     * definir período de interesse
#     * definir tipo de agregação (=processamento)
#     * executar leitura
# 5. **Leitura** de anotações
#     * definir variável de interesse
#     * definir período de interesse
#     * executar leitura
# 6. **Escrita** de valores escalares
#     * definir variável de interesse
#     * definir valor, timestamp e qualidade
#     * executar escrita
# 7. **Escrita** de valores históricos
#     * definir variável de interesse
#     * definir vetor de valores, timestamps e qualidades
#     * executar escrita
# 8. **Escrita** de anotações
#     * definir variável de interesse
#     * definir mensagem e timestamp
#     * executar escrita
# 9. **CRUD** (Create, Read, Update and Delete) de variáveis - não faz parte do escopo deste minicurso
# 10. **Encerramento da Conexão** (=sessão) com um **EPM Server** (=servidor de dados)

# 1. **Estabelecimento de Conexão** (=sessão) com um **EPM Server** (=servidor de dados)

# In[99]:


# No ambiente Jupyter - fazer gráfico no próprio ambiente usando a MATPLOTLIB
get_ipython().run_line_magic('matplotlib', 'inline')

# Importação dos princiapais módulos utilizados em análises de dados de processo
# Dica:
# Sempre procurar tratar as exceções para facilitar a manutenção dos códigos e a utilização por terceiros!
try:
    import numpy as np
    import datetime
    import pytz
    import matplotlib.pyplot as plt
    import pandas as pd
    # Importação do módulo para conecão com o EPM Server (via EPM Web Server)
    import epmwebapi as epm
    print('Módulos importados com sucesso!')
except ImportError as error:
    print('Erro na importação!')
    print(error.__class__.__name__ + ': ' + error.message)
except Exception as exception:
    print(exception.__class__.__name__ + ': ' + exception.message)


# In[100]:


# ATENÇÃO:
# Para uso em produção, é recomendado usar variáveis de ambiente para buscar informações de Usuário/Senha.
# Para este minicurso será utilizado as funções input e getpass
import getpass
user = input('EPM user:')
password = getpass.getpass("EPM password:")
epm_auth = 'http://epmtr.elipse.com.br/auth' # 'http://localhost:44333'
epm_web  = 'http://epmtr.elipse.com.br'# 'http://localhost:44332'

# Criação de uma conexão informando os endereços do EPM Webserver(Authentication Port e WEB API Port), usuário e senha.
try:
    epmConn = epm.EpmConnection(epm_auth, epm_web, user, password)
    # A forma mais recomendada (fácil) para usar o comando print é com fstring
    print(f'Conexão com {epm_web} criada com sucesso para o usuário {user}.')
except:
    print(f'Falha no estabelecimento da conexão com {epm_web} para o usuário {user}.')


# 2. **Criação** das variáveis de interesse

# In[101]:


# DICA:
# Definir uma lista com as variáveis de interesse para facilitar seu uso/reuso
bvList = ['LIC101', 'FIC101']
bvDic = epmConn.getDataObjects(bvList)
bv_LIC101 = bvDic[bvList[0]]
bv_FIC101 = bvDic[bvList[1]]
print('Nível do tanque: {}'.format(bv_LIC101)) # outra forma de usar o comando print é com o método format
print('Válvula do tanque: {}'.format(bv_FIC101))


# ### Dica
# 
# ###### É possível usar filtros para pesquisar as variáveis de interesse e criá-las no ambiente Python.
# 
# ###### *exemplo*: é possível que se busque por todas as variáveis que tenham °C como unidade de medida.
# 
# ###### Exemplos de uso de filtros podem ser vistos no GitHub da Elipse Software:
# [Elipse Software/epmwebapi/exemplos/Quickstart.ipynb](https://nbviewer.jupyter.org/github/elipsesoftware/epmwebapi/blob/master/exemplos/Quickstart.ipynb)

# #### Usando as funções *dir* para ver métodos-propriedades e filtro com regex sobre strings para eliminar os métodos-propriedades "privados"

# In[102]:


import re
# DICA: https://regex101.com/
regex = re.compile(r'[^\b_]') # <=> Não iniciar palavra com _
all_meth_props = dir(bv_LIC101)
meth_props = list(filter(regex.match, all_meth_props))
print(*meth_props, sep=" | ")


# #### Por padrão, *name* é a única propriedade lida do EPM Server para criação da *Basic Variable* no ambiente Python.

# In[103]:


# Por padrão, a única propriedade que
print(f'Variável: {bv_LIC101.name}')
print(f'Descrição: {bv_LIC101.description }')
print(f'Unidade de Medida (= E.U.): {bv_LIC101.eu}')


# #### Quando for necessário saber o valor destas propriedades, é necessário: (i) criar a variávle no ambiente Python solicitando que estes valores sejam lidos na criação da mesma; (ii) proceder com a leitura destas propriedades sob demanda após a criação da mesma.

# In[104]:


# Exemplo de busca das propriedades da variável bv_LIC101 (previamente criada)
bv_LIC101.readAttributes()
print(f'Variável: {bv_LIC101.name}')
print(f'Descrição: {bv_LIC101.description }')
print(f'Unidade de Medida (= E.U.): {bv_LIC101.eu}')


# 3. **Leitura** de valores escalares
# 
# #### Lê o último valor proveniente da via de tempo real do EPM Server: (i) via *Interface de Comunicação*; (ii) via escrita com o método *write*.
# 
# #### Valores inseridos na base de dados através: (i) restauração de bkp; (ii) uso do EPM Tag Port (); (iii)  função historyUpdate;  só são acessados através de consultas históricas, como historyRead e historyReadAggregate.

# In[105]:


# Trazendo par ao ambiebte Python uma variável que tem dados provenientes da via de tempo real (rand01)
rand01 = epmConn.getDataObjects(['rand01'])['rand01']
last_value = rand01.read()
print(f'Último valor recebido pela via de tempo real: {last_value.value}')
print(f'Último timestamp associado ao valor: {last_value.timestamp}')
print(f'Última qualidade associada ao valor: {last_value.statusCode} - 0 corresponde à "Good" no Padrão OPC UA')
# Nota:
# No padrão OPC DA Classic 192 corresponde à qualidade "Good"


# 4. **Leitura** de valores históricos
# 
# ##### Valores brutos (raw) - como foram armazenados
# ##### Agregação - padrão OPC UA
# 

# In[139]:


# Consulta dos valores "brutos" (= raw data)
# Valores "devem" ser informados em conforemidade com o Timezone ou em UTC (Coordinated Universal Time)
ini_date = datetime.datetime(2014, 3, 4, 2, tzinfo=pytz.utc)
end_date = datetime.datetime(2014, 3, 4, 4, tzinfo=pytz.utc)
query_period = epm.QueryPeriod(ini_date, end_date)
data = bv_LIC101.historyReadRaw(query_period)

#plt.plot(data['Timestamp'], data['Value'], color='b')
plt.plot(data['Value'], color='#00e6e6')
plt.legend(loc='lower right')
plt.xlabel("Time")
plt.ylabel(bv_LIC101.name + '[' + bv_LIC101.eu['displayName'] + ']')

# Notas extras:
# Redimensionando e colorindo a figura posteriormente á sua criação
fig = plt.gcf()
ax = plt.gca()
fig.set_size_inches(18, 10)
fig.patch.set_facecolor('#525454')
ax.set_facecolor('#323434')
#fig.savefig(bv_LIC101.name + '.png', dpi=100) # salvar imagem em arquivo

# ATENÇÃO!
# Os Timestamps retornados estão sempre em UTC!
print(data[0])


# In[136]:


dir(fig.patch.axes)


# #### Regras de ouro quando se trabalha com Timestamps
# 
# * Sempre usar objetos datetime "offset-aware" (delta do local em relação ao UTC).
# * Sempre armazenar datetime em UTC e fazer a conversão do fuso horário apenas ao interagir com usuários.
# * Sempre usar a norma internacional ISO 8601 como entrada/saída para repersentações de data-hora.
# 
# ##### Exemplos norma ISO 8601
# 
# * Data: 2019-07-16
# * Data e horas separados, em UTC: 2019-07-16 21:02Z
# * Data e horas combinadas, em UTC: 2019-07-16T21:02Z
# * Data com número da semana: 2019-W29-2
# * Data ordinal: 2019-197

# In[ ]:


# Nota:
# UTC’ is Coordinated Universal Time. It is a successor to, but distinct from, Greenwich Mean Time (GMT) and the various definitions of Universal Time. UTC is now the worldwide standard for regulating clocks and time measurement.
# All other timezones are defined relative to UTC, and include offsets like UTC+0800 - hours to add or
# subtract from UTC to derive the local time. No daylight saving time occurs in UTC, making it a useful
# timezone to perform date arithmetic without worrying about the confusion and ambiguities caused by
# daylight saving time transitions, your country changing its timezone, or mobile computers that roam
# through multiple timezones.
#
# ref.: http://pytz.sourceforge.net/
#
# Verificar os timezones que iniciam por 'America/S'  -> para mostrar Sao_Paulo
print(list(filter(lambda s: s.find('America/S')+1, pytz.common_timezones)))
print(50 * '#')
# ATENÇÃO!
# Wrong value returned from offset for timezones in Brazil
# https://github.com/sdispater/pendulum/issues/319
#
tz_sp = pytz.timezone('America/Sao_Paulo')
ini_date1 = datetime.datetime(2014, 3, 3, 23, tzinfo=tz_sp)
end_date1 = datetime.datetime(2014, 3, 4, 1, tzinfo=tz_sp)
query_period1 = epm.QueryPeriod(ini_date1,end_date1)
data1 = bv_LIC101.historyReadRaw(query_period1)

# Para colocar o OFF-SET manualmente, deve-se primeiro identificá-lo (ou informar manualmente)
now_naive = datetime.datetime.now() # Só para ver que existe um método NOW!
now_aware = datetime.datetime.utcnow() # Usado para identificar o OFFSET
localize = pytz.utc.localize(now_aware) # # Só para ver que existe um método localize!
now_sp = now_aware.astimezone(tz_sp) # Usado para identificar o OFFSET
print(f'Data-hora agora simples, sem informações de Timezone: {now_naive}')
print(f'Data-hora agora com informações de Timezone:          {now_aware}')
print(f'Localização UTC - Timezone:                           {localize}')
print(f'Localização São Paulo - Timezone:                     {now_sp}')
print(50 * '#')
tz_offset = now_sp.tzinfo.utcoffset(now_aware).seconds/(3600) - 24 # is_dst=False -> sem horário de verão!
tz_ok = datetime.timezone(datetime.timedelta(hours=tz_offset))
# tz_ok = -3 # São Paulo (Brasília) - Brasil - sem horário de verão!
ini_date2 = datetime.datetime(2014, 3, 3, 23, tzinfo=tz_ok)
end_date2 = datetime.datetime(2014, 3, 4, 1, tzinfo=tz_ok)
query_period2 = epm.QueryPeriod(ini_date2,end_date2)
data_ok = bv_LIC101.historyReadRaw(query_period2)
# Imprimindo resultado final!
print('Timestamp com problemas: {}'.format(data1[0]))
print('Timestamp OK: {}'.format(data_ok[0]))


# In[ ]:





# In[ ]:


dir(now_sp)


# In[ ]:


dir(now_sp.tzinfo)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# 5. **Leitura** de anotações

# In[ ]:





# In[ ]:





# ### Dica
# 
# ###### Ver exemplo de uso de anotações no GitHub da Elipse Software: [Elipse Software/epmwebapi/exemplos/sample01.ipynb](https://nbviewer.jupyter.org/github/elipsesoftware/epmwebapi/blob/master/exemplos/sample01.ipynb)

# 6. **Escrita** de valores escalares

# In[ ]:





# 7. **Escrita** de valores históricos

# In[ ]:





# 8. **Escrita** de anotações

# 9. **CRUD** (Create, Read, Update and Delete) de variáveis - não faz parte do escopo deste minicurso

# 10. **Encerramento da Conexão** (=sessão) com um **EPM Server** (=servidor de dados)

# In[ ]:


# SEMPRE deve-se encerrar a conexão estabelecida com o EPM Server, pois isso irá encerrar a sessão e
# liberar a licença de EPM Client para que outros, eventualmente, possam utilizá-la.
epmConn.close()


# ## _FIM dos exemplos ..._
# 
# #### Retornar à apresentação
