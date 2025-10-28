import bs4 ,requests ,re ,json

#1. 取得書名、價格、評分
#2. 每一本書存在<atricle class='product_pod'>容器
#3. 書名存在<h3>標籤內的title屬性
#4. 價格存在<p class='price_color>內
#5. 評分存在<p class='star-rating (number)'>

url = 'https://books.toscrape.com/catalogue/category/books_1/index.html'
books = []

if __name__ == '__main__':
    
    try:
        response = requests.get(url)
    
    except requests.exceptions.HTTPError as e:
    
        print(f'{url} 請求失敗')
        exit(1)
    
    soup = bs4.BeautifulSoup(response.text ,'lxml')
    
    article_tags = soup.find_all('article' ,attrs={'class':'product_pod'})
    
    for container in article_tags:

        title  = container.find('h3').a.get('title')
        price  = container.find('p' ,attrs={'class':'price_color'}).text
        rating = container.find('p' ,attrs={'class':re.compile('star-rating [One|Two|Three|Four|Five]')}).get('class')[1]

        books.append({'title':title ,'price':re.search('£[0-9]*.[0-9]{2}' ,price).group() ,'rating':rating})

    print(json.dumps(books ,ensure_ascii=False ,indent=2))