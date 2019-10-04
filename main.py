import requests
import json
import os
from dotenv import load_dotenv


def user_link(token):
  url1 = "https://api-ssl.bitly.com/v4/user"
  headers = { 
    "Authorization" : "Bearer "+token,
  }
  response = requests.get(url1, headers=headers)
  response.raise_for_status()
  pretty_profile = json.dumps(response.json(), indent=2)
  print(pretty_profile)


def shorten_link(token, url):
  url2 = "https://api-ssl.bitly.com/v4/bitlinks"
  headers = { 
    "Authorization" : "Bearer "+token,
  }
  payload = {
    "long_url" : url
  }
  response = requests.post(url2, headers=headers, json=payload)
  response.raise_for_status()
  bitlink = response.json()['link']
  return bitlink


def count_clicks(token, url):
  blink = url[url.rfind("//")+1:]
  url3 = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(blink)
  headers = { 
    "Authorization" : "Bearer "+token,
  }
  payload = {
    "units" : "-1",
  }
  response = requests.get(url3, headers=headers, params=payload)
  response.raise_for_status()
  clicks_count = response.json()['total_clicks'] 
  return clicks_count

def main():
  load_dotenv()
  token = os.getenv("TOKEN_BITLY")
  url = input("Введите ссылку: ")
  user_link(token)
  if url.startswith("http://bit.ly"):
    try:
      clicks_count = count_clicks(token, url)
      print(count_clicks(token, url)) 
    except requests.exceptions.HTTPError:
      print("Неверно введен битлинк")
  else:
    try:
      bitlink = shorten_link(token, url)
      print('Битлинк', shorten_link(token, url))
    except requests.exceptions.HTTPError:
      print("Неверно введена ссылка")

if __name__ == "__main__":
  main()
