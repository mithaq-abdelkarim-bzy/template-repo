from html.parser import HTMLParser

class HTMLToText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
    
    def handle_data(self, data):
        self.text.append(data)
    
    def handle_starttag(self, tag, attrs):
        if tag in ("br", "p", "div"):
            self.text.append("\n")
    
    def handle_endtag(self, tag):
        if tag in ("p", "div"):
            self.text.append("\n")

def html_to_text(html):
    if not html or html.strip() == "":
        return ""

    parser = HTMLToText()
    parser.feed(html)
    parser.close()

    return "".join(parser.text).strip()
