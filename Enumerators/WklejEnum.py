import requests
import webbrowser
from BeautifulSoup import BeautifulSoup
import sys
import os
import threading

def enum(start, stop):

    baseUrl = "http://www.wklej.org/id/"
    rangeWidth = stop-start
    lock = threading.Lock()

    for i in range (start,stop + 1):
        urlStr = baseUrl+str(i)
        rResponse = requests.get(urlStr).text

        html = rResponse
        parsed_html = BeautifulSoup(html)
        foundResult = parsed_html.find('td', attrs={'class':'code'})
        if foundResult != None:
            gitResp = foundResult.text
            iGotIt = False

            if "cda" in gitResp and "&lt;a href=&quot;" not in gitResp and "ahref=&quot;" not in gitResp:
                iGotIt = True
            elif "premium" in gitResp and "&lt;a href=&quot;" not in gitResp and "ahref=&quot;" not in gitResp:
                iGotIt = True
            elif "Premium" in gitResp and "&lt;a href=&quot;" not in gitResp and "ahref=&quot;" not in gitResp:
                iGotIt = True

            if iGotIt:
                lock.acquire()
                try:
                    with open("FoundUrls.txt", "a") as myfile:
                        myfile.write(urlStr+"\n")
                    print urlStr
                finally:
                    lock.release()

            iGotIt = False

        if i % 10 == 0:
            percentDone = float(i-start) / float(rangeWidth) * 100
            print "%.2f%%" %percentDone

    print "Search completed 100%"

baseUrl = "http://www.wklej.org/id/"
countFrom = 3151200
openedUrlsCounter = 0

for i in range(200):

    child = threading.Thread(target = enum , args = (countFrom - 100, countFrom ,))
    child.start()
    print "From: %d To: %d" % (countFrom - 100,countFrom )
    countFrom = countFrom - 100

mainThread = threading.currentThread()
for t in threading.enumerate():
    if t is not mainThread:
        t.join()
print "\nAll threads ended their work \nOpening sites\n"

with open ("FoundUrls.txt") as f:
    allUrls = f.readlines()

allUrls = [x.strip() for x in allUrls]

for url in allUrls:
    openedUrlsCounter = openedUrlsCounter + 1
    if openedUrlsCounter % 11 == 0:
        print "To open next 10 found sites press any key"
        sys.stdin.read(1)
    savOut = os.dup(1)
    savErrOut = os.dup(2)
    os.close(1)
    os.close(2)
    os.open(os.devnull, os.O_RDWR)
    try:
        webbrowser.open(url)
    finally:
         os.dup2(savOut, 1)
         os.dup2(savErrOut, 2)
