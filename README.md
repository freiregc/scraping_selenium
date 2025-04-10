# **Aplicação RPA: Scraping do Google Imagens usando a bibloteca Selenium**

## **Primeiros passos para executar os comandos**

1. Criar ambiente virtual (venv):

    1.1. Execute o comando a seguir para criar o ambiente virtual para rodar o código:

    ```sh
    python -m venv venv
    ```

    1.2. Após a criação do ambiente virtual, ative-o com o comando:

    ```sh
    .\venv\Scripts\activate
    ```

    - Para desativar o ambiente virtual, execute o comando a seguir:

        ```sh
        deactivate
        ```

2. Instale as dependências necessárias:

    2.1. Com o ambiente virtual ativado, execute o comando a seguir para instalar as dependências:

    ```sh
    pip install -r requirements.txt
    ```

    - Valide a instalação das dependências:

        ```sh
        pip freeze
        ```
    
    2.2. Por fim, atualize o pip com o comando:

    ```sh
    python.exe -m pip install --upgrade pip
    ```