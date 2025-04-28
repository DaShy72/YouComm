from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


def count_scrols(URL):
    # Настройки браузера
    options = Options()
    # НЕ включаем headless режим
    options.add_argument("--headless=new")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

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

    # Открываем YouTube
    try:
        video_url = URL
        driver.get(video_url)
    except:
        return ("Error: Ivalid URL")

    # Ждём загрузки страницы
    time.sleep(5)

    driver.execute_script("window.scrollTo(0, 600);")
    time.sleep(2)

    try:
        # Ищем нужный тег
        comment_count = driver.find_element(
            By.CSS_SELECTOR,
            "yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer span.style-scope.yt-formatted-string"
        )
        count = comment_count.text
        count = count.replace(' ', '')
        result = (int(count) // 20) + 1
        return result
    except Exception as e:
        return ("Error:", e)

    driver.quit()
