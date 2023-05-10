import os
import sys
import requests
from bs4 import BeautifulSoup
import threading
import shutil
import time

sys.path.append(os.path.abspath('./'))

from utils import gen_headers

host = 'http://www.bzxgt.com'
root_path = './bzxgt_imgs/'
threads = []

def get_home_nav():
  print('请求首页......')
  r = requests.get(host, headers=gen_headers())
  soup = BeautifulSoup(r.text, 'html5lib')
  nav_a = soup.find(class_='top_nav').find_all('a')
  print('请求成功......')
  print('选择一个分类: ')
  for i, a in enumerate(nav_a):
    if not a.text == '首页':
      print(f'{i}. {a.text}')
  
  user_input = input('请输入一个编号来选择: ')

  sub_url = nav_a[int(user_input) - 1].get('href')
  sub_name = nav_a[int(user_input) - 1].text

  get_sub_list(sub_url, sub_name)

def get_sub_list(url, name):
  print('请求分类页面: ' + url)
  r = requests.get(url, headers=gen_headers())
  soup = BeautifulSoup(r.text, 'html5lib')
  dls = soup.find(class_='chanpin_list').find_all('dl')
  print('请求成功......')

  folder = os.path.join(root_path, name)
  print('创建分类文件夹, 已存在则自动跳过......')
  os.makedirs(folder, exist_ok=True)

  print('开始批量爬取子页面......')
  for i, dl in enumerate(dls):
    a = dl.find('dd').find('a')
    title = a.text
    url = a.get('href')
    thread = threading.Thread(target=get_content, args=(url, title, folder))
    threads.append(thread)
    thread.start()

def get_content(url, title, folder):
  print('爬取子页面: ' + url)
  r = requests.get(url, headers=gen_headers())
  soup = BeautifulSoup(r.text, 'html5lib')
  imgs = soup.find(class_='neirong_body').find_all('img')

  real_path = os.path.join(folder, title)
  os.makedirs(real_path, exist_ok=True)

  for img in imgs:
    filename = f'{title}{int(time.time() * 1000)}'
    download_img(img.get('src'), filename, real_path)
    time.sleep(2)

def download_img(url, name, folder):
  print('开始下载图片:' + url)
  r = requests.get(url, headers=gen_headers(), stream=True)
  ext = r.headers.get('Content-Type').split('/')[1]
  filename = f'{name}.{ext}'
  file_path = os.path.join(folder, filename)
  with open(file_path, 'wb') as f:
    shutil.copyfileobj(r.raw, f)
    print('图片下载成功: ' + file_path)

if (__name__ == '__main__'):
  get_home_nav()
