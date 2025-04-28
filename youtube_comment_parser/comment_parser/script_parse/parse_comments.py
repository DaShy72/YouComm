from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from .count_comment import count_scrols
from selenium.webdriver.chrome.options import Options


def parse_comment(URL):
    # URL видео с комментариями
    YOUTUBE_VIDEO_URL = URL

    count = count_scrols(YOUTUBE_VIDEO_URL)

    # Настройки браузера
    options = Options()
    # НЕ включаем headless режим
    options.add_argument("--headless=new")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    # Запускаем драйвер
    driver = webdriver.Chrome(options=options)

    # Убираем признак автоматизации
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
           Object.defineProperty(navigator, 'webdriver', {
             get: () => undefined
           })
           """
    })

    # Запуск браузера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(YOUTUBE_VIDEO_URL)
        time.sleep(5)  # Ждём загрузки страницы

        # Прокручиваем страницу вниз несколько раз для загрузки комментариев
        scroll_pause_time = 5
        last_height = driver.execute_script("return document.documentElement.scrollHeight")

        for _ in range(count):
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Собираем комментарии
        comments = driver.find_elements(By.CSS_SELECTOR, "#content #content-text")

        result_comments = []

        for comment in comments:
            result_comments.append(comment.text)

        return result_comments
        print(f"✅ Успешно сохранено {len(comments)} комментариев в 'comments.txt'.")

    except Exception as e:
        return (f"❌ Ошибка: {e}")

    finally:
        driver.quit()