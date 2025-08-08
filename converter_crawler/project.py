from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import zh_converter 


     


# 設定 Chrome 選項
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

service = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://tw.carousell.com/categories/women-s-fashion-4/")
    print("頁面加載完成")
    
    # 等待初始內容加載
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid^='listing-card']"))
    )
    
    # 滾動並加載更多內容
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(2):  # 嘗試滾動2次
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 等待新內容加載
        
        # 檢查是否有「顯示更多結果」的按鈕並點擊
        try:
            load_more_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '顯示更多結果') or contains(text(), 'Show more results')]"))
            )
            driver.execute_script("arguments[0].click();", load_more_button)
            print("點擊了「顯示更多結果」按鈕")
            time.sleep(3)  # 等待新內容加載
        except:
            pass  # 如果找不到按鈕或不可點擊，則繼續
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("已到達頁面底部，停止滾動")
            break
        last_height = new_height
    
    # 獲取所有商品
    products = driver.find_elements(By.CSS_SELECTOR, "div[data-testid^='listing-card']")
    print(f"找到 {len(products)} 個商品")
    

    empty_dict = {}
    # 提取商品資訊
    for product in products:
        try:
            name = product.find_element(By.CSS_SELECTOR, "p[style^='--max']").text
            price = product.find_element(By.CSS_SELECTOR, "p[title^='NT$']").text
            name = zh_converter.converter(name) #翻譯
            print(f"商品:{name}  | 價格: {price}")
        except Exception as e:
            print(f"提取商品時出錯: {e}")
            continue
            
except Exception as e:
    print(f"發生錯誤: {e}")
finally:
    driver.quit()