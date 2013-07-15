from bs4 import BeautifulSoup

def getCorrectTree(text):
    html = BeautifulSoup(text)
    return html.prettify(formatter="xml")
