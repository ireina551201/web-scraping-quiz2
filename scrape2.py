import bs4 ,requests ,re ,json

url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'
books = []

if __name__ == '__main__':
    
    # HTTP請求
    try:

        response = requests.get(url)
        
        if response.status_code != 200:

            raise requests.exceptions.HTTPError(f',狀態碼: {response.status_code}')

    except requests.exceptions.HTTPError as e:
        
        print(f'{url}請求失敗' ,e)
        exit(1)
    
    # 解析:
    #   1. 每一本書各自存放在 <atricle class='product_pod'> 容器裡
    #   2. 書名存在 <atricle class='product_pod'> --> <h3> 標籤內的title屬性
    #   3. 價格存在 <atricle class='product_pod'> --> <p class='price_color> 內
    #   4. 評分存在 <atricle class='product_pod'> --> <p class='star-rating [number]'>
    soup = bs4.BeautifulSoup(response.text ,'lxml')
    
    article_tags = soup.find_all('article' ,attrs={'class':'product_pod'})
    
    for container in article_tags:

        title  = container.find('h3').a.get('title')
        price  = container.find('p' ,attrs={'class':'price_color'}).text
        rating = container.find('p' ,attrs={'class':re.compile('star-rating [One|Two|Three|Four|Five]')}).get('class')[1]

        books.append({'title':title ,'price':re.search('£[0-9]*.[0-9]{2}' ,price).group() ,'rating':rating})

    # 輸出
    print(json.dumps(books ,ensure_ascii=False ,indent=2))