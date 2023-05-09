from fake_useragent import UserAgent

def gen_headers():
  return {
    'User-Agent': UserAgent().chrome
  }
