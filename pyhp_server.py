import os, sys
import BaseHTTPServer, urlparse
from cStringIO import StringIO

PATH = "web"
write_header = """out=''
def write(text):
    global out
    out += text

"""
context = {'out':''}


mypath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"lib")
sys.path.append(mypath)

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def handle_error(self,code,message):
        self.send_response(code)
        self.wfile.write("""
            <html>
            <title>
                %d : %s
            </title>
            <body>
            <h1>%d : %s</h1>
            </body>
            </html>
            """ % (code, message,code, message))

    def do_GET(self):
        global PATH, context
        self.do_POST()

    def do_POST(self):
        global PATH, context
        mypath = self.path.split('?',1)
        filename = PATH+mypath[0]
        print filename
        data = ""
        args = {}
        if 'Content-Length' in self.headers.keys():
        	length = int(self.headers['Content-Length'])
        	args = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
        elif len(mypath) > 1:
        	args = urlparse.parse_qs(mypath[1])
        try:
            with open(filename,"r") as fp:
                data = fp.read()
        except Exception:
            return self.handle_error(404,"file %s not found"%filename)
        self.send_response(200)
        #self.send_header("Content-type", "text/html")
        self.end_headers()
        context['args']=args
        self.wfile.write(parse_file(data, context))

def run_while_true(server_class=BaseHTTPServer.HTTPServer,
                   handler_class=Handler):
    """
    This assumes that keep_running() is a function of no arguments which
    is tested initially and after each request.  If its return value
    is true, the server continues.
    """
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    while True:
        httpd.handle_request()

def parse_file(text,context):
    i=0
    mode = "html"
    open_index = -1
    while(i<len(text)):
        if mode == "html":
            if text[i] == "<":
                if text[i+1] == "?":
                    i=i+1
                    mode = "pyhp"
                    open_index = i+1
        if mode == "pyhp":
            if text[i] == "?":
                if text[i+1] == ">":
                    #print text[open_index:i]
                    ret = compile(write_header+text[open_index:i],"<string>","exec")
                    context['out']=""
                    exec(ret,context,{})
                    text = text[:open_index-2]+context['out']+text[i+2:]
                    return parse_file(text,context)
        i = i+1
    return text






if __name__ == "__main__":
    run_while_true()