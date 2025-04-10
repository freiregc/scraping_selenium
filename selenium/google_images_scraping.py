from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from urllib.request import urlopen
from shutil import copyfileobj
import numpy as np

'''
Este código realiza o scraping das imagens do Google Imagens através
da biblioteca Selenium.

Acompanhe as instruções do README para executar o código sem maiores problemas. 
'''

# Variável para armazenar qual a pesquisa que será feita no Google Imagens
pesquisa = input('Digite o que deseja buscar no Goole Imagens: ')

# Instância o Chrome webdriver para a execução do scraping de imagens
chrome_options = Options()

# Desabilita a extensão de automação do Chrome, evitando a detecção da automação
chrome_options.add_experimental_option("useAutomationExtension", False)

# Exclui o parâmetro "enable-automation" da linha de comando do Chrome para evitar sinais de automação
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Permite que o navegador continue aberto após o término do script
chrome_options.add_experimental_option("detach", True)

# Cria uma instância do WebDriver do Chrome, com as opções definidas acima
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Abre o Google Imagens no navegador
driver.get('https://images.google.com/')

# Maximiza a janela do navegador
driver.maximize_window()

# Encontra a caixa de pesquisa na página do Google Imagens
caixa_pesquisa = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea')

# Digita o termo de pesquisa na caixa de pesquisa
caixa_pesquisa.send_keys(pesquisa)

# Pressiona "Enter" para iniciar a pesquisa
caixa_pesquisa.send_keys(Keys.ENTER)

# Aguarda 1 segundo para garantir que a página carregue os resultados
time.sleep(1)

# Variável para controle de quando a imagem for encontrada
encontrou_imagem = False

# Função para rolar até o final da página e carregar mais resultados
def scroll_para_baixo():
    # Obtém a altura atual da página
    ultima_altura_pagina = driver.execute_script('return document.body.scrollHeight')

    # Continua rolando até o final da página
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')

        # Aguarda o carregamento dos novos resultados
        time.sleep(5)

        # Obtém a nova altura da página
        nova_altura_pagina = driver.execute_script('return document.body.scrollHeight')

        # Tenta clicar no botão "Mostrar mais resultados" (se existir)
        try:
            driver.find_element_by_css_selector(".YstHxe input").click()

            # Aguarda o carregamento dos resultados
            time.sleep(5)

        except:
            pass

        # Verifica se a página foi rolada até o final
        if nova_altura_pagina == ultima_altura_pagina:
            break

        ultima_altura_pagina = nova_altura_pagina

# Chama a função para rolar até o final da página e carregar mais imagens
scroll_para_baixo()

try:
    # Encontra todas as imagens na página usando um seletor XPath
    imagens = driver.find_elements(By.XPATH, "//img[@class='YQ4gaf']")

    # Variável para controle do nome do arquivo de cada imagem
    nome_arquivo = 1
    
    # Loop para baixar todas as imagens encontradas
    for imagem in imagens:
        # Imprime o URL da imagem
        print(imagem.get_attribute('src'))
        
        # Obtém o URL da imagem
        src = imagem.get_attribute('src')
        
        # Baixa a imagem e salva no disco com um nome único
        nome_arquivo += 1
        with urlopen(src) as in_stream, open(f'{nome_arquivo}.png', 'wb') as out_file:
            copyfileobj(in_stream, out_file)
        
        # Aguarda 0.2 segundos antes de baixar a próxima imagem para evitar bloqueios
        time.sleep(0.2)

except Exception as e:
    # Caso ocorra algum erro ao tentar baixar as imagens, exibe o erro
    print(e)
    pass

# Fecha o navegador após o término do script
driver.close()
