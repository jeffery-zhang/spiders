import os
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import threading
import random

host = 'https://www.871651.com'
root_img_path = './imgs/'
headers = {
  'User-Agent': UserAgent().chrome,
}

if not os.path.exists(root_img_path):
  os.mkdir(root_img_path)

def get_home_nav():
  ''' 获取首页导航并返回导航名称和链接列表 '''
  result = []
  response = requests.get(host, headers=headers)
  soup = BeautifulSoup(response.text, 'html5lib')
  nav_ul = soup.find(class_='nav')
  for nav_a in nav_ul.find_all('a'):
    result.append({
      'href': nav_a.get('href'),
      'name': nav_a.text,
    })
  return result

def user_choose(categories):
  ''' 通过获取的导航列表让用户选择一个导航分类 '''
  options = set([f'{str(index + 1)}. {item["name"]}' for index, item in enumerate(categories)])
  options_sorted = sorted(options, key=lambda x: int(x.split('. ')[0]))
  print('请选择一个分类: ')
  for item in options_sorted:
    print(item)
  user_input = input('请输入一个编号来选择: ')
  selected_name = options_sorted[int(user_input) - 1].split('. ')[1]

  dirname = os.path.join(root_img_path, selected_name)

  if not os.path.exists(dirname):
    os.mkdir(dirname)
  for c in categories:
    if selected_name == c['name']:
      get_sub_page(c, dirname)
    
def get_sub_page(chosed, dirname):
  response = requests.get(chosed['href'], headers=headers)
  soup = BeautifulSoup(response.text, 'html5lib')
  list_ul = soup.find('ul', class_='list')
  list_a = list_ul.find_all('a')
  # for article in list_a:
  article = list_a[0]
  article_href = article.get('href')
  article_name = article.find('h3').text
  real_path = os.path.join(dirname, article_name)
  os.makedirs(real_path, exist_ok=True)
  get_content(article_href, real_path)

def get_content(url, path):
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html5lib')
  target = soup.find('div', class_='news_article')
  all_img = target.find_all('img')

  imgs = []

  for img in all_img:
    img_src = img.get('src')
    img_name = img.get('alt')
    imgs.append({
      'url': img_src,
      'name': img_name,
    })

  multi_download(imgs, path)

def download_one(url, file_name):
  print(f'正在下载: {url}')
  r = requests.get(url)
  with open(file_name, 'wb') as f:
    f.write(r.content)
  print(f'下载完成: {url}')

def multi_download(imgs, real_path):
  threads = []
  print(imgs)
  for img in imgs:
    file_name = os.path.join(real_path, img['name'])
    thread = threading.Thread(target=download_one, args=(img['url'], file_name))
    threads.append(thread)
    thread.start()

  for thread in threads:
    thread.join()

if (__name__ == '__main__'):
  categories = get_home_nav()
  user_choose(categories)
