import re ,requests

url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'

if __name__ == '__main__':

    # HTTP請求
    try:

        response = requests.get(url)
        
        if response.status_code != 200:

            raise requests.exceptions.HTTPError(f',狀態碼: {response.status_code}')

    except requests.exceptions.HTTPError as e:
        
        print(f'{url}請求失敗' ,e)
        exit(1)
    
    # 解析
    prices_list = re.findall('£[0-9]*.[0-9]{2}' ,response.text)

    #輸出
    print(prices_list)