import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DOWNLOAD_FOLDER = "imagens"


def criar_pasta(nome_pesquisa: str) -> str:
    """Cria a pasta de destino para salvar as imagens."""
    caminho = os.path.join(DOWNLOAD_FOLDER, nome_pesquisa.replace(" ", "_"))
    os.makedirs(caminho, exist_ok=True)
    return caminho


def iniciar_driver() -> webdriver.Chrome:
    """Inicia o Chrome com opções otimizadas para scraping."""
    opcoes = Options()
    opcoes.add_argument("--start-maximized")
    opcoes.add_argument("--disable-blink-features=AutomationControlled")
    opcoes.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=opcoes)
    return driver


def pesquisar_imagens(driver: webdriver.Chrome, pesquisa: str) -> None:
    """Navega até o Google Images e realiza a pesquisa."""
    driver.get("https://www.google.com/imghp?hl=pt-BR")
    wait = WebDriverWait(driver, 10)
    campo_busca = wait.until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    campo_busca.send_keys(pesquisa)
    campo_busca.send_keys(Keys.ENTER)
    time.sleep(2)


def scroll_para_carregar(driver: webdriver.Chrome, quantidade_scrolls: int = 10) -> None:
    """Faz scroll na página para carregar todas as imagens."""
    print("\n[*] Fazendo scroll para carregar imagens...\n")
    
    for i in range(quantidade_scrolls):
        # Scroll até o final da página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"  Scroll {i+1}/{quantidade_scrolls}...")
        time.sleep(2)
        
        # Tenta clicar no botão "Mostrar mais resultados" se existir
        try:
            botoes = driver.find_elements(By.CSS_SELECTOR, "input[type='button']")
            for botao in botoes:
                if botao.is_displayed():
                    botao.click()
                    print("  → Botão 'Mostrar mais' clicado")
                    time.sleep(3)
                    break
        except Exception:
            pass


def coletar_urls_imagens(driver: webdriver.Chrome) -> list[str]:
    """Coleta as URLs de todas as imagens carregadas na página."""
    print("\n[*] Coletando URLs das imagens...\n")
    
    # Pega todas as imagens com a classe YQ4gaf
    imagens = driver.find_elements(By.XPATH, "//img[@class='YQ4gaf']")
    
    print(f"  {len(imagens)} imagens encontradas!\n")
    
    urls: list[str] = []
    urls_set: set[str] = set()
    
    for img in imagens:
        try:
            # Tenta pegar o src ou data-src
            src = img.get_attribute("src")
            if not src:
                src = img.get_attribute("data-src")
            
            # Valida se é uma URL válida
            if src and src.startswith("http") and src not in urls_set:
                urls.append(src)
                urls_set.add(src)
                print(f"  [{len(urls)}] URL coletada")
        except Exception:
            continue
    
    return urls


def baixar_imagens(urls: list[str], pasta: str) -> None:
    """Faz o download das imagens coletadas."""
    print(f"\n[*] Baixando {len(urls)} imagens para '{pasta}'...\n")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"
    }

    sucesso = 0
    for i, url in enumerate(urls, start=1):
        try:
            resposta = requests.get(url, headers=headers, timeout=10)
            resposta.raise_for_status()

            extensao = "jpg"
            content_type = resposta.headers.get("Content-Type", "")
            if "png" in content_type:
                extensao = "png"
            elif "webp" in content_type:
                extensao = "webp"
            elif "gif" in content_type:
                extensao = "gif"

            caminho_arquivo = os.path.join(pasta, f"imagem_{i:03d}.{extensao}")
            with open(caminho_arquivo, "wb") as f:
                f.write(resposta.content)

            sucesso += 1
            print(f"  [{i}/{len(urls)}] Salva: {caminho_arquivo}")
        except Exception as e:
            print(f"  [{i}/{len(urls)}] Erro ao baixar: {e}")

    print(f"\n[✓] Download concluído! {sucesso}/{len(urls)} imagens salvas em '{pasta}'.")


def main():
    print("=" * 50)
    print("  Web Scraping - Google Images")
    print("=" * 50)

    pesquisa = input("\nDigite o termo de pesquisa: ").strip()
    if not pesquisa:
        print("Nenhum termo informado. Encerrando.")
        return

    pasta = criar_pasta(pesquisa)
    driver = iniciar_driver()

    try:
        pesquisar_imagens(driver, pesquisa)
        scroll_para_carregar(driver, quantidade_scrolls=10)
        urls = coletar_urls_imagens(driver)

        if not urls:
            print("\n[!] Nenhuma imagem encontrada.")
            return

        baixar_imagens(urls, pasta)
    except KeyboardInterrupt:
        print("\n\n[!] Interrompido pelo usuário.")
    except Exception as e:
        print(f"\n[!] Erro inesperado: {e}")
    finally:
        driver.quit()
        print("\n[*] Navegador fechado.")


if __name__ == "__main__":
    main()
