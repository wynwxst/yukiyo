import easyjson
import requests
from bs4 import BeautifulSoup
import base64
import os

class W:
  def __init__(self):
    self.db = easyjson.use("prefabs/prefabs.json")
    self.url = self.db.data["webtoons.com"]["url"]
    self.ep = self.db.data["webtoons.com"]["ep"]
    self.query = self.db.data["webtoons.com"]["search"]
    self.api = False
    if self.query == "api":
      self.api = True
      self.query = self.db.data["webtoons.com"]["api"]
  def loadimg(self,image_obj):
    i = image_obj

    url = i['url']
    h = i["h"]
    w = i["w"]
    if os.name == 'nt':
        user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      'AppleWebKit/537.36 (KHTML, like Gecko)' 
                      'Chrome/92.0.4515.107 Safari/537.36')
    else:
        user_agent = ('Mozilla/5.0 (X11; Linux ppc64le; rv:75.0)' 
                      'Gecko/20100101 Firefox/75.0')
    headers = {
        'dnt': '1',
        'user-agent': user_agent,
        'accept-language': 'en-US,en;q=0.9',
    }
    image_headers = {
        'referer': 'https://www.webtoons.com/',
        **headers
    }
    r = requests.request("GET",url=url,headers=image_headers)
    uri = ("data:" + 
       r.headers['Content-Type'] + ";" +
       "base64," + base64.b64encode(r.content).decode("utf-8"))
    return f"<img src='{uri}' width='{w}' height='{h}'/>"
  def viewimg(self,image_obj):
    i = image_obj

    url = i['url']
    h = i["h"]
    w = i["w"]
    if os.name == 'nt':
        user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      'AppleWebKit/537.36 (KHTML, like Gecko)' 
                      'Chrome/92.0.4515.107 Safari/537.36')
    else:
        user_agent = ('Mozilla/5.0 (X11; Linux ppc64le; rv:75.0)' 
                      'Gecko/20100101 Firefox/75.0')
    headers = {
        'dnt': '1',
        'user-agent': user_agent,
        'accept-language': 'en-US,en;q=0.9',
    }
    image_headers = {
        'referer': 'https://www.webtoons.com/',
        **headers
    }
    r = requests.request("GET",url=url,headers=image_headers)
    uri = ("data:" + 
       r.headers['Content-Type'] + ";" +
       "base64," + base64.b64encode(r.content).decode("utf-8"))
    return f"<img src='{uri}' width='{w}' height='{h}' class='centeral'/>"
  def search(self,q):
    su = ""
    su = self.query.replace("{q}",q)
    r = requests.request("GET",url=su)
    #card_lst
    soup = BeautifulSoup(r.text,"html5lib").find('ul',class_='card_lst').find_all("li")
    obj = {}
    c = 1
    for a in soup:
      hyper = a.find("a")
      icon = a.find("img")
      div = a.find("a").find("div", class_="info")
      title = div.find("p", class_="subj")
      title = str(title).split(">")
      title = title[1]
      title = title.replace("</p","")
      
      author = div.find("p", class_="author")
      author = str(author).split(">")
      author = author[1]
      author = author.replace("</p","")
      genre = a.find("span")
      genre
      a_obj = {}
      a_obj["title"] = str(hyper["href"]).replace("/episodeList?titleNo=","")
      icon = {"h":str(icon["height"]),"w":str(icon["width"]),"url":str(icon["src"])}
      a_obj["icon"] = icon
      
      a_obj["name"] = title
      a_obj["author"] = author
      obj[str(c)] = a_obj
      c += 1
      
    
    return obj
      
  def loadbanner(self,image_obj):
      i = image_obj
      url = i
      if os.name == 'nt':
          user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                        'AppleWebKit/537.36 (KHTML, like Gecko)' 
                        'Chrome/92.0.4515.107 Safari/537.36')
      else:
          user_agent = ('Mozilla/5.0 (X11; Linux ppc64le; rv:75.0)' 
                        'Gecko/20100101 Firefox/75.0')
      headers = {
          'dnt': '1',
          'user-agent': user_agent,
          'accept-language': 'en-US,en;q=0.9',
      }
      image_headers = {
          'referer': 'https://www.webtoons.com/',
          **headers
      }
      r = requests.request("GET",url=url,headers=image_headers)
      uri = ("data:" + 
         r.headers['Content-Type'] + ";" +
         "base64," + base64.b64encode(r.content).decode("utf-8"))
      return uri
  def search(self,q):
    su = ""
    su = self.query.replace("{q}",q)
    r = requests.request("GET",url=su)
    #card_lst
    soup = BeautifulSoup(r.text,"html5lib").find('ul',class_='card_lst').find_all("li")
    obj = {}
    c = 1
    for a in soup:
      hyper = a.find("a")
      icon = a.find("img")
      div = a.find("a").find("div", class_="info")
      title = div.find("p", class_="subj")
      title = str(title).split(">")
      title = title[1]
      title = title.replace("</p","")
      
      author = div.find("p", class_="author")
      author = str(author).split(">")
      author = author[1]
      author = author.replace("</p","")
      genre = a.find("span")
      genre
      a_obj = {}
      a_obj["title"] = str(hyper["href"]).replace("/episodeList?titleNo=","")
      icon = {"h":str(icon["height"]),"w":str(icon["width"]),"url":str(icon["src"])}
      a_obj["icon"] = icon
      
      a_obj["name"] = title
      a_obj["author"] = author
      obj[str(c)] = a_obj
      c += 1
      
    
    return obj
  def series(self,t):
    t = str(t)
    url = self.url
    url = url.replace("{title}",t)
    r = requests.request("GET",url=url)
    day = BeautifulSoup(r.text,"html5lib").find('p',class_='day_info')
    day = str(day).split("EVERY")
    day = day[-1]
    day = day.replace("</p>","")
    day = day.replace(" ","")
    day = day.lower()
    div = BeautifulSoup(r.text,"html5lib").find("div", class_="info")
    title = div.find("h1", class_="subj")
    title = str(title).split(">")
    title = title[1]
    title = title.replace("</h1","")

    banner = BeautifulSoup(r.text,"html5lib").find("span",class_="thmb").find("img")["src"]
    desc = BeautifulSoup(r.text,"html5lib").find('p',class_='summary')
    eps = BeautifulSoup(r.text,"html5lib").find('li', attrs={'data-episode-no': True}).find('a')['href'].split('&')[1]
    eps = eps.replace("episode_no=","")
    icon = BeautifulSoup(r.text,"html5lib").find('li', attrs={'data-episode-no': True}).find('span').find("img")
    icon = {"h":str(icon["height"]),"w":str(icon["width"]),"url":str(icon["src"])}
    obj = {}
    obj["title"] = t
    obj["icon"] = icon
    obj["episodes"] = str(eps)
    obj["description"] = desc
    obj["day"] = day
    obj["name"] = title
    obj["banner"] = banner
    return obj
  def episode(self,series_obj,ep):
    ep = str(ep)
    iep = int(ep)
    s = series_obj
    url = self.ep
    url = url.replace("{title}",s["title"])
    url = url.replace("{ep}",ep)
    
    r = requests.request("GET",url=url)
    
    soup = BeautifulSoup(r.text, 'lxml')
    x = soup.find('div', class_='viewer_img _img_viewer_area').find_all('img')
    c = 1
    ep_obj = {}
    
    for i in x:
      i_obj = {}
      i_obj["url"] = i["data-url"]
      i_obj["h"] = i["height"]
      i_obj["w"] = i["width"]

        
      ep_obj[str(c)] = i_obj
      c += 1
    #ep_obj["next"] = str( iep + 1)
    #ep_obj["back"] = str( iep - 1)
    return ep_obj
      
    