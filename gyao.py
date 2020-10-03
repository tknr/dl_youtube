from requests_html import HTMLSession
import re

url = "https://gyao.yahoo.co.jp/p/01081/v00136/"

session = HTMLSession()
r = session.get(url)
r.html.render()

title = r.html.search('<p class="video-player-title">{}</p>')[0]

year = re.sub("\\D","",r.html.search('<small>{}</small>')[0])

print(title + " (" + str(year) + ")")

