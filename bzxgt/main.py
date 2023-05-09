import os
import sys
import requests
from bs4 import BeautifulSoup
import threading

sys.path.append(os.path.abspath('./'))

from utils import gen_headers

host = 'http://www.bzxgt.com'
root_path = './bzxgt_imgs/'
threads = []

def get_home_nav():
  r = requests.get(host, headers=gen_headers())
  soup = BeautifulSoup(r.text, 'html5lib')
  nav_a = soup.find(class_='top_nav').find_all('a')
  print('选择一个分类: ')
  for i, a in enumerate(nav_a):
    if not a.text == '首页':
      print(f'{i + 1}. {a.text}')
  
  user_input = input('请输入一个编号来选择: ')

  sub_url = nav_a[int(user_input) - 1].get('href')
  sub_name = nav_a[int(user_input) - 1].text

  get_sub_list(sub_url, sub_name)

def get_sub_list(url, name):
  r = requests.get(url, headers=gen_headers())
  soup = BeautifulSoup(r.text, 'html5lib')
  dls = soup.find(class_='chanpin_list').find_all('dl')

  folder = os.path.join(root_path, name)
  os.makedirs(folder, exist_ok=True)

  for dl in dls:
    a = dl.find('dd').find('a')
    title = a.text
    url = a.get('href')
    thread = threading.Thread(target=get_content, args=(url, title, folder))
    threads.append(thread)
    thread.start()

def get_content(url, title, folder):
  r = requests.get(url, headers=gen_headers())
  soup = BeautifulSoup(r.text, 'html5lib')
  imgs = soup.find(class_='neirong_body').find_all('img')

  real_path = os.path.join(folder, title)
  os.makedirs(real_path, exist_ok=True)

  print(url, title)

if (__name__ == '__main__'):
  get_home_nav()
