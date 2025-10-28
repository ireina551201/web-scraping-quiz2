import requests ,bs4 ,re ,json

#1. 所有書籍資訊存放在<li class='item'>標籤內
#2. 排行存放在<strong class='no'>標籤
#3. 價格存放在<li class="price_a">優惠價：<strong><b>79</b></strong>折<strong><b>[價格]</b></strong>元</li>

url = 'https://www.books.com.tw/web/sys_saletopb/books/19?attribute=30'
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
    
    # 解析
    soup = bs4.BeautifulSoup(response.text ,'lxml')

    container = soup.select_one('div.mod_a.clearfix')

    items = container.find_all('li' ,attrs={'class':'item'})

    for content in items:
        
        title     = content.find('img' ,attrs={'class':'cover'}).get('alt')
        raw_price = content.select_one('li.price_a').text
        rank      = content.select_one('strong.no').text

        price = re.search('([0-9]*)元' ,raw_price).group(1)

        books.append({'title':title ,'price':f'NT${price}' ,'rank':rank})
    
    # 輸出
    print(json.dumps(books ,ensure_ascii=False ,indent=2))