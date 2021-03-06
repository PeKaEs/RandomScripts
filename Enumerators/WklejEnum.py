import requests
import webbrowser
from BeautifulSoup import BeautifulSoup
import sys
import os
import threading
from lxml import html

def enum(start, stop, listOfPatterns, listOfAntiPatterns, baseUrl):

    rangeWidth = stop-start
    lock = threading.Lock()
    threadSession = requests.Session()

    for i in range (start,stop + 1):
        urlStr = baseUrl+str(i)

        try:
            rResponse = threadSession.get(urlStr).text
        except:
            continue

        parsed_html = html.fromstring(rResponse)
        foundResult = parsed_html.cssselect("td.code")

        if foundResult != None and foundResult != []:
            gitResp = foundResult[0].text_content()
            iGotIt = False

            if any(antiPattern in gitResp for antiPattern in listOfAntiPatterns):
                continue
            if any(pattern in gitResp for pattern in listOfPatterns):
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
countFrom = 3153014
openedUrlsCounter = 0
patternList = ["cda", "premium", "Premium", "haslo", "Haslo", "haselko", "Haselko", "pass", "password", "Pass", "Password"]
antiPatternList = ["&lt;a href=&quot;", "ahref=&quot;", "else", "void", "include", "Farbar Recovery Scan Tool", "(FRST)", "<a href=", "ahref", "Uruchomiony przez"]

for x in range(10):
    for i in range(1000):

        child = threading.Thread(target = enum , args = (countFrom - 100, countFrom ,patternList, antiPatternList, baseUrl ))
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
