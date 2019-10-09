import requests
import json
import os
from dotenv import load_dotenv
import argparse


def shorten_link(token, url):
  url_request = "https://api-ssl.bitly.com/v4/bitlinks"
  headers = { 
    "Authorization" : "Bearer "+token,
  }
  payload = {
    "long_url" : url
  }
  response = requests.post(url_request, headers=headers, json=payload)
  response.raise_for_status()
  bitlink = response.json()['link']
  return bitlink


def count_clicks(token, url):
  bitlink = url[url.rfind("//")+1:]
  url_request = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(bitlink)
  headers = { 
    "Authorization" : "Bearer "+token,
  }
  payload = {
    "units" : "-1",
  }
  response = requests.get(url_request, headers=headers, params=payload)
  response.raise_for_status()
  clicks_count = response.json()['total_clicks'] 
  return clicks_count

def main():
  load_dotenv()
  token = os.getenv("TOKEN_BITLY")
  parser = argparse.ArgumentParser(description="url in bitly or counter bitly")
  parser.add_argument('url', type=str, help='Input URL')
  args = parser.parse_args()
  url = args.url

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
