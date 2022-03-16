### repl/local/normal

import os
import sys
try:
  from flask import Flask,render_template,request,send_file,make_response
  import easyjson
  from funcs import Prefabs as p
except ImportError:
  os.system("bash scripts/deps.sh")
  from flask import Flask,render_template,request,send_file,make_response
  import easyjson
  from funcs import Prefabs as p
w = p.webtoons
app = Flask('app')
app.config["url"] = "https://quiet-taiga-00976.herokuapp.com/"

def render_page(content,theme,ao="",at="",ath="",af="",next="",title="",back="",t="page"):
  # 'active-link'
  if theme == None:
    theme = "white"
  url = app.config["url"]
  return render_template(f"{t}.html",content=content,ao=ao,at=at,ath=ath,af=af,theme=theme,next=next,title=title,back=back,url=url)

@app.route('/favicon.ico/')
def favicon():
  return send_file("static/logo.png")

@app.route('/query/')
def query():
  return render_template("search.html",theme=request.cookies.get("theme"),url=app.config["url"])
@app.route('/viewer/')
def viewer():
  title = request.args.get("title")
  ep = request.args.get("ep")
  if title == None or ep == None:
    return "specify args"
  html = """\n\n<title>""" +  title + """</title>\n
  <style>
  .view_div {

  line-height: 300px;
  text-align: center;
}

.centeral {
  vertical-align: middle;
}
  </style>

  """
  s = w.series(title)
  imgs = w.episode(s, ep)
  for obj in imgs:
    html += "\n<div class='view_div'>\n" + w.viewimg(imgs[obj]) + "\n</div>\n"
  return render_page(content=html,theme=request.cookies.get("theme"),title=title,next=str(int(ep)+1),back=str(int(ep)-1),t="viewer")


@app.route('/search/')
def search():
  q = request.args.get("q")
  q = q.replace("%20"," ")

  if q == None :
    return "specify args"
  html = """\n<style>\n /* Font */
@import url('https://fonts.googleapis.com/css?family=Quicksand:400,700');

/* Design */
*,
*::before,
*::after {
  box-sizing: border-box;
}

html {
  background-color: #ffffff;
}

body {
  color: #000000;
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
          <a href=" """ + app.config["url"] + """/preview?title={title}">
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
  return render_page(content=html,theme=request.cookies.get("theme"),at="active-link")



@app.route('/preview/')
def preview():
  q = request.args.get("title")

  if q == None :
    return "specify args"
  html = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
* {box-sizing: border-box;}

body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  background-color: white
}

.topnav {
  overflow: hidden;
  background-color: #FFC0CB;
}

.topnav a {
  float: left;
  display: block;
  color: black;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
}

.topnav a:hover {
  background-color: #ddd;
  color: black;
}

.topnav a.active {
  background-color: #2196F3;
  color: white;
}

.topnav .search-container {
  float: right;
}

.topnav input[type=text] {
  padding: 6px;
  margin-top: 8px;
  font-size: 17px;
  border: none;
}

.topnav .search-container button {
  float: right;
  padding: 6px 10px;
  margin-top: 8px;
  margin-right: 16px;
  background: #ddd;
  font-size: 17px;
  border: none;
  cursor: pointer;
}

.topnav .search-container button:hover {
  background: #ccc;
}

@media screen and (max-width: 600px) {
  .topnav .search-container {
    float: none;
  }
  .topnav a, .topnav input[type=text], .topnav .search-container button {
    float: none;
    display: block;
    text-align: left;
    width: 100%;
    margin: 0;
    padding: 14px;
  }
  .topnav input[type=text] {
    border: 1px solid #ccc;
  }
}
</style>
  \n<style>
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
  background-color: #fffff;
}

body {
  color: #000000;
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
  color: white;
  background-color: #FFC0CB;
  opacity: 0.3;
  text-align: center;
  cursor: pointer;
}

.hero-text button:hover {
  background-color: #555;
  opacity: 0.9
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
    <a href='""" + app.config["url"] + """/viewer?title={title}&ep=1'>
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
          <a href=" """ + app.config["url"] + """/viewer?title={title}&ep={ep}">
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
  return render_page(content=html,theme=request.cookies.get("theme"))

@app.route("/set/")
def set():

  theme = request.args.get("bg")
  resp = make_response(render_template('loading.html',theme=theme,r=app.config["url"] + "/settings"))
  resp.set_cookie('theme', theme)
  return resp

@app.route("/settings/")
def settings():
  html = """
  <!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {
  box-sizing: border-box;
}

input[type=text], select, textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
}

label {
  padding: 12px 12px 12px 0;
  display: inline-block;
}

input[type=submit] {
  background-color: #04AA6D;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  float: right;
}

input[type=submit]:hover {
  background-color: #45a049;
}

.container {
  border-radius: 5px;

  padding: 20px;
}

.col-25 {
  float: left;
  width: 25%;
  margin-top: 6px;
}

.col-75 {
  float: left;
  width: 75%;
  margin-top: 6px;
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}

/* Responsive layout - when the screen is less than 600px wide, make the two columns stack on top of each other instead of next to each other */
@media screen and (max-width: 600px) {
  .col-25, .col-75, input[type=submit] {
    width: 100%;
    margin-top: 0;
  }
}
</style>
</head>
<body>


<div class="container">
  <form action="/set">
    <div class="row">
      <div class="col-25">
        <label for="fname">Color background</label>
      </div>
      <div class="col-75">
        <input type="text" id="bg" name="bg" placeholder="Eg. 'blue','black'">
      </div>
    </div>
    <div class="row">
      <div class="col-25">
      </div>
      <div class="col-75">

      </div>
    </div>
    <div class="row">
      <input type="submit" value="Save">
    </div>
  </form>
</div>

</body>
</html>
"""
  return render_page(content=html,theme=request.cookies.get("theme"),af="active-link")
#index
@app.route("/")
def index():
  return render_template("index.html",url=app.config["url"])

@app.route('/loading/')
def loading():
  url = app.config["url"]
  r = request.args.get("r")
  if r == None:
    r = url
  else:
    r = r.replace("^","?")
    r = r.replace("|","&")
    r =  url + "/" + r
  return render_template("loading.html",theme=request.cookies.get("theme"),r=r)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
# try simple render with webtoons.com
