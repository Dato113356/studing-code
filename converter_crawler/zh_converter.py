import requests
import re

def fetch_php_file_from_github():
    url = "https://raw.githubusercontent.com/wikimedia/mediawiki/master/includes/languages/data/ZhConversion.php"

    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"無法獲取檔案，狀態碼: {response.status_code}")

def parse_conversion_data(php_content):
    # 使用正則表達式提取對應資料
    pattern = r"'(.*?)' => '(.*?)'"
    matches = re.findall(pattern, php_content)
    conversion_dict = {traditional: simplified for traditional, simplified in matches}  # 反轉字典
    return conversion_dict

class ZhConversion:
    def __init__(self, conversion_dict):
        self.conversion_dict = conversion_dict

    def convert_to_simplified(self, text):
        # 按照鍵的長度從長到短排序
        sorted_keys = sorted(self.conversion_dict.keys(), key=len, reverse=True)

        for traditional in sorted_keys:
            text = text.replace(traditional, self.conversion_dict[traditional])
        return text

    

def converter(self):
    # 獲取 PHP 檔案內容
    php_content = fetch_php_file_from_github()

    # 解析轉換資料
    conversion_data = parse_conversion_data(php_content)

    # 建立翻譯器實例
    translator = ZhConversion(conversion_data)

    # 用戶輸入
    text = translator.convert_to_simplified(self)
    return text

if __name__ == "__main__":
    # 獲取 PHP 檔案內容
    php_content = fetch_php_file_from_github()

    # 解析轉換資料
    conversion_data = parse_conversion_data(php_content)

    # 建立翻譯器實例
    translator = ZhConversion(conversion_data)

    # 用戶輸入
    user_input = input("請輸入要轉換的字串：")
    converted_text = translator.convert_to_simplified(user_input)
    print(converted_text)
   
