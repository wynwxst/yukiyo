from flask import Flask,render_template,request
import easyjson
from funcs import Prefabs as p
w = p.webtoons
app = Flask('app')

@app.route('/viewer/')
def viewer():
  title = request.args.get("title")
  ep = request.args.get("ep")
  if title == None or ep == None:
    return "specify args"
  html = """\n\n<title>""" +  title + """</title>\n
  <style>
  div {

  line-height: 300px; 
  text-align: center;    
}

div img {
  vertical-align: middle;
}
  </style>
  
  """
  s = w.series(title)
  imgs = w.episode(s, ep)
  for obj in imgs:
    html += "\n<div>\n" + w.loadimg(imgs[obj]) + "\n</div>\n"
  return html
  

@app.route('/search/')
def search():
  q = request.args.get("q")
  q = q.replace("%20"," ")
  
  if q == None :
    return "specify args"
  html = """<style>\n /* Font */
@import url('https://fonts.googleapis.com/css?family=Quicksand:400,700');

/* Design */
*,
*::before,
*::after {
  box-sizing: border-box;
}

html {
  background-color: #ecf9ff;
}

body {
  color: #272727;
  font-family: 'Quicksand', serif;
  font-style: normal;
  font-weight: 400;
  letter-spacing: 0;
  padding: 1rem;
}

.main{
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
    font-size: 24px;
    font-weight: 400;
    text-align: center;
}

img {
  height: auto;
  max-width: 100%;
  vertical-align: middle;
}

.btn {
  color: #ffffff;
  padding: 0.8rem;
  font-size: 14px;
  text-transform: uppercase;
  border-radius: 4px;
  font-weight: 400;
  display: block;
  width: 100%;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: transparent;
}

.btn:hover {
  background-color: rgba(255, 255, 255, 0.12);
}

.cards {
  display: flex;
  flex-wrap: wrap;
  list-style: none;
  margin: 0;
  padding: 0;
}

.cards_item {
  display: flex;
  padding: 1rem;
}

@media (min-width: 40rem) {
  .cards_item {
    width: 50%;
  }
}

@media (min-width: 56rem) {
  .cards_item {
    width: 33.3333%;
  }
}

.card {
  background-color: white;
  border-radius: 0.25rem;
  box-shadow: 0 20px 40px -14px rgba(0, 0, 0, 0.25);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.card_content {
  padding: 1rem;
  background: linear-gradient(to bottom left, #EF8D9C 40%, #FFC39E 100%);
}

.card_title {
  color: #ffffff;
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: capitalize;
  margin: 0px;
}

.card_text {
  color: #ffffff;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1.25rem;    
  font-weight: 400;
}
.made_by{
  font-weight: 400;
  font-size: 13px;
  margin-top: 35px;
  text-align: center;
}
</style>
  \n  <div class="main">
  <h1>Search Results:</h1>
  <ul class="cards">\n"""
  r_temp = """
  \n

    <li class="cards_item">
      <div class="card">
        <div class="card_image">{load_img}
        <div class="card_content">
          <h2 class="card_title">{name}</h2>
          <p class="card_text">By {author}</p>
          <a href="https://yukiyo.ehnryu.repl.co/preview?title={title}">
          <button class="btn card_btn">Read</button>
          </a>
        </div>
      </div>
    </li>\n
  """
  r = w.search(q)
  for item in r:
    t = r_temp
    for v in r[item]:
      if v != "icon":
        t = t.replace("{" + v +"}",str(r[item][v]))
      else:
        ic = w.loadimg(r[item][v])
        t = t.replace("{load_img}",ic)
    html += "\n" + t + "\n"
        
      
  html += "\n"
  html += "  </ul>\n</div>"
  return html



@app.route('/preview/')
def preview():
  q = request.args.get("title")
  
  if q == None :
    return "specify args"
  html = """<style>
body, html {
  height: 100%;
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
}
\n /* Font */
@import url('https://fonts.googleapis.com/css?family=Quicksand:400,700');

/* Design */
*,
*::before,
*::after {
  box-sizing: border-box;
}

html {
  background-color: #ecf9ff;
}

body {
  color: #272727;
  font-family: 'Quicksand', serif;
  font-style: normal;
  font-weight: 400;
  letter-spacing: 0;
  padding: 1rem;
}

.main{
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
    font-size: 24px;
    font-weight: 400;
    text-align: center;
}

img {
  height: auto;
  max-width: 100%;
  vertical-align: middle;
}

.btn {
  color: #ffffff;
  padding: 0.8rem;
  font-size: 14px;
  text-transform: uppercase;
  border-radius: 4px;
  font-weight: 400;
  display: block;
  width: 100%;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: transparent;
}

.btn:hover {
  background-color: rgba(255, 255, 255, 0.12);
}

.cards {
  display: flex;
  flex-wrap: wrap;
  list-style: none;
  margin: 0;
  padding: 0;
}

.cards_item {
  display: flex;
  padding: 1rem;
}

@media (min-width: 40rem) {
  .cards_item {
    width: 50%;
  }
}

@media (min-width: 56rem) {
  .cards_item {
    width: 33.3333%;
  }
}

.card {
  background-color: white;
  border-radius: 0.25rem;
  box-shadow: 0 20px 40px -14px rgba(0, 0, 0, 0.25);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.card_content {
  padding: 1rem;
  background: linear-gradient(to bottom left, #EF8D9C 40%, #FFC39E 100%);
}

.card_title {
  color: #ffffff;
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: capitalize;
  margin: 0px;
}

.card_text {
  color: #ffffff;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1.25rem;    
  font-weight: 400;
}
.made_by{
  font-weight: 400;
  font-size: 13px;
  margin-top: 35px;
  text-align: center;
}


.hero-text {
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
}

.hero-text button {
  border: none;
  outline: 0;
  display: inline-block;
  padding: 10px 25px;
  color: black;
  background-color: #ddd;
  text-align: center;
  cursor: pointer;
}

.hero-text button:hover {
  background-color: #555;
  color: white;
}
  .wrapper {
  display: flex;
  justify-content: space-around;
}
.button {
  background-color: linear-gradient(to bottom left, #EF8D9C 40%, #FFC39E 100%);
  border: none;
  color: white;
  padding: 16px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  transition-duration: 0.4s;
  cursor: pointer;
}
.episode {
  width: 100%;
  background-color: linear-gradient(to bottom left, #EF8D9C 40%, #FFC39E 100%)
  color: white; 

}

  .hero-image{
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('{banner}');
  height: 50%;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  position: relative;
}
  \n</style>\n\n
  <div class="hero-image">
  <div class="hero-text">
    <h1 style="font-size:50px">{name}</h1>
    <a href='https://yukiyo.ehnryu.repl.co/viewer?title={title}&ep=1'>
    <button class="btn card_btn">Episode 1</button>
    </a>
    <p> {description} </p>
    <p> Every {day} </p>
  </div>
</div>\n
  <div class="main">
  <h1>Episodes</h1>
  <ul class="cards">\n"""
  r_temp = """
    <li class="cards_item">
      <div class="card">

        <div class="card_content">
          <p class="card_text">{number}</p>
          <a href="https://yukiyo.ehnryu.repl.co/viewer?title={title}&ep={ep}">
          <button class="btn card_btn">Read</button>
          </a>
        </div>
      </div>
    </li>\n
  
  \n
  """
  r = w.series(q)
  title = r["title"]
  
  for item in r:
    if item not in ["icon","banner"]:
      html = html.replace("{" + item + "}",str(r[item]))
    if item == "banner":
      banner = w.loadbanner(r[item])
      html = html.replace("{" + "banner" + "}",str(banner))
  eps = int(r["episodes"])
  while float(eps) != 0:
    t = r_temp
    t = t.replace("{title}",str(title))
    t = t.replace("{ep}",str(eps))
    t = t.replace("{number}","Episode " + str(eps))
    eps -= 1
    
    html += "\n" + t + "\n"
        
      
  html += "\n"
  html += "  </ul>\n</div>"
  return html

@app.route("/")
def index():
  return render_template("index.html")

app.run(host='0.0.0.0', port=8080,debug=True)
# try simple render with webtoons.com