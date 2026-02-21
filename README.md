# Web Scraping - Google Images

Script automatizado para fazer download de imagens do Google Images usando Selenium.

## 📋 O que o código faz

Este script permite fazer scraping (raspagem) de imagens do Google Images de forma automatizada:

1. **Solicita um termo de pesquisa** ao usuário
2. **Abre o Google Images** automaticamente no navegador Chrome
3. **Faz scroll pela página** 10 vezes para carregar o máximo de imagens possível
4. **Coleta as URLs** de todas as imagens encontradas (geralmente 400-500 imagens)
5. **Baixa todas as imagens** automaticamente para uma pasta organizada
6. **Salva no formato original** (JPG, PNG, WebP ou GIF)

As imagens são salvas na pasta `imagens/<termo_pesquisa>/` com nomes sequenciais (`imagem_001.jpg`, `imagem_002.png`, etc.).

## 🔧 Pré-requisitos

- **Python 3.12+**
- **Google Chrome** instalado no sistema
- **uv** (gerenciador de pacotes Python)

## 🚀 Preparando o ambiente

### 1. Instalar o uv (se ainda não tiver)

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clonar ou baixar o projeto

```powershell
cd C:\Users\Gabriel\Desktop\Projetos\scraping
```

### 3. Instalar as dependências

```powershell
uv sync
```

Isso instalará automaticamente:
- `selenium` (automação do navegador)
- `requests` (download de imagens)

## 📖 Como usar

Execute o script:

```powershell
uv run main.py
```

O script irá:
1. Solicitar o termo de pesquisa (ex: "colher", "cachorro", "paisagem")
2. Abrir o Chrome automaticamente
3. Fazer scroll e carregar as imagens
4. Baixar todas as imagens encontradas

**Exemplo de uso:**

```
==================================================
  Web Scraping - Google Images
==================================================

Digite o termo de pesquisa: gato

[*] Fazendo scroll para carregar imagens...
  Scroll 1/10...
  ...

[*] Coletando URLs das imagens...
  500 imagens encontradas!

[*] Baixando 500 imagens para 'imagens\gato'...
  [1/500] Salva: imagens\gato\imagem_001.jpg
  [2/500] Salva: imagens\gato\imagem_002.png
  ...

[✓] Download concluído! 498/500 imagens salvas em 'imagens\gato'.
```

## 📁 Estrutura de pastas

Após a execução, as imagens serão organizadas assim:

```
scraping/
├── imagens/
│   ├── gato/
│   │   ├── imagem_001.jpg
│   │   ├── imagem_002.png
│   │   └── ...
│   └── colher/
│       ├── imagem_001.jpg
│       └── ...
├── main.py
├── pyproject.toml
└── README.md
```

## ⚙️ Funcionalidades principais

### `criar_pasta(nome_pesquisa)`
Cria a pasta de destino para salvar as imagens organizadamente.

### `iniciar_driver()`
Inicializa o Chrome com configurações otimizadas para scraping (maximizado, sem notificações).

### `pesquisar_imagens(driver, pesquisa)`
Navega até o Google Images e realiza a busca pelo termo informado.

### `scroll_para_carregar(driver)`
Faz scroll automático pela página 10 vezes para carregar mais resultados. Tenta clicar no botão "Mostrar mais resultados" quando disponível.

### `coletar_urls_imagens(driver)`
Localiza todas as imagens usando XPATH (`//img[@class='YQ4gaf']`) e extrai suas URLs.

### `baixar_imagens(urls, pasta)`
Faz o download de todas as URLs coletadas, detecta o formato (JPG, PNG, WebP, GIF) e salva com nomes sequenciais.

## ⚠️ Observações

- **Velocidade**: O script aguarda alguns segundos entre scrolls e downloads para evitar sobrecarga
- **Falhas**: Algumas imagens podem falhar no download (URLs expiradas, bloqueios). O script continua e reporta o sucesso ao final
- **Quantidade**: O número de imagens varia (geralmente 400-500) dependendo do termo de pesquisa
- **ChromeDriver**: O Selenium 4+ gerencia automaticamente o ChromeDriver, não é necessário baixá-lo manualmente

## 🛠️ Tecnologias utilizadas

- **Python 3.12+**
- **Selenium 4.41+** - Automação do navegador
- **Requests 2.32+** - Download de imagens HTTP
- **uv** - Gerenciamento de dependências

## 📝 Licença

Projeto livre para uso educacional e pessoal.

---

**Desenvolvido com ❤️ usando Python e Selenium**
