from bottle import route, run, request, template,static_file
import requests
import os
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR,'static')

@route('/static/css/<filename:path>')
def send_static(filename):
    return static_file(filename,root=f'{STATIC_DIR}/css')

@route('/')
def index(): 
    response = requests.get('https://www.hermes.com/jp/ja/category/women/bags-and-small-leather-goods/bags-and-clutches/#|')
    
    soup = BeautifulSoup(response.text,'html.parser')

    #クラス名「product-item-name」のh4タグにバックの名称の文字列
    items_bag = soup.find_all('h4',class_='product-item-name')
    #クラス名「product-item-price」のdivタグにバックの値段の文字列
    bags_price = soup.find_all('div',class_='product-item-price')
    #クラス名「product-item-colors」のspanタグにバックのカラーの文字列
    bags_color = soup.find_all('span',class_='product-item-colors')
    #クラス名「default-image」のdivタグのHTMLを取得
    get_imageId = soup.find_all('div',class_="default-image")

    #imgタグのidを取得するための前処理
    get_imageId_list_dummy = []
    for i in range(len(get_imageId)):
        get_imageId_list_dummy.append(get_imageId[i].prettify())

    #imgタグのidを配列に格納する
    get_imageId_list = []
    for i in range(len(get_imageId_list_dummy)):
        get_imageId_list.append(get_imageId_list_dummy[i][get_imageId_list_dummy[i].find('img-H'):get_imageId_list_dummy[i].find('img-H')+15])

    #スクレイピングしたバックの名称、値段、色、imgタグのidを格納する配列を作成
    bags_list = []

    #名称、値段、色、imgタグのidを一つのまとまりとする１行4列の配列を作成し、その配列をbags_list配列に要素として追加する
    for i in range(len(bags_price)):
        dummy_list = []
        dummy_list.append(items_bag[i].text)
        dummy_list.append(bags_price[i].text.split()[1])#値段の文字列から、¥○○のところだけを取得
        dummy_list.append(bags_color[i].text.split()[2])#色の文字列から、色名のところだけを取得 
        dummy_list.append(get_imageId_list[i])
        bags_list.append(dummy_list)#bags_list配列に１行2列の配列を追加する

    context_data = {
        'bags_list':bags_list
    }
    
    return template('index',**context_data)

if __name__ == "__main__":
    run(host='localhost', port=8080, reloader = True ,debug=True)



