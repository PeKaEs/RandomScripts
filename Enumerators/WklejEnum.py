import requests
import webbrowser
#try:
from BeautifulSoup import BeautifulSoup
import thread
#except ImportError:
    #from bs4 import BeautifulSoup


def enum(start,stop):

    baseUrl = "http://www.wklej.org/id/"
    for i in range (start,stop + 1):
        urlStr = baseUrl+str(i)
        rResponse = requests.get(urlStr).text

        html = rResponse
        parsed_html = BeautifulSoup(html)
        elo = parsed_html.find('td', attrs={'class':'code'})
        if elo != None:
            gitResp = elo.text
            if "cda" in gitResp and "&lt;a href=&quot;" not in gitResp and "ahref=&quot;" not in gitResp:
                webbrowser.open(urlStr)
            elif "premium" in gitResp and "&lt;a href=&quot;" not in gitResp and "ahref=&quot;" not in gitResp:
                webbrowser.open(urlStr)
            elif "Premium" in gitResp and "&lt;a href=&quot;" not in gitResp and "ahref=&quot;" not in gitResp:
                webbrowser.open(urlStr)

        if i%2 == 0:
            print (str((float(i)/(float(stop) + 1)*100)) + "%")

baseUrl = "http://www.wklej.org/id/"
countFrom = 3145827

for i in range(300):
    try:
        thread.start_new_thread( enum, (countFrom - 10,countFrom , ) )
    except:
        print "Error: unable to start thread"
    countFrom = countFrom - 10
while 1:
    pass
