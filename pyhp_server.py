import os
import sys
import http.server
import urllib.parse as urlparse
from io import StringIO
from socketserver import ThreadingMixIn

PATH = "web"
write_header = """__out=''
def write(text):
    global __out
    __out += text

"""
context = {'__out': ''}


mypath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
sys.path.append(mypath)


class ThreadingHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    pass


class Handler(http.server.BaseHTTPRequestHandler):

    def handle_error(self, code, message):
        self.send_response(code)
        self.wfile.write(bytes("""
            <html>
            <title>
                %d : %s
            </title>
            <body>
            <h1>%d : %s</h1>
            </body>
            </html>
            """ % (code, message, code, message), "UTF-8"))

    def do_GET(self):
        global PATH, context
        self.do_POST()

    def do_POST(self):
        global PATH, context
        mypath = self.path.split('?', 1)
        if mypath[0] == "/":
            mypath[0] = "/index.pyhp"
        filename = PATH + mypath[0]
        print(filename)
        data = ""
        args = {}
        if 'Content-Length' in self.headers.keys():
            length = int(self.headers['Content-Length'])
            args = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
        elif len(mypath) > 1:
            args = urlparse.parse_qs(mypath[1])
        try:
            with open(filename, "r") as fp:
                data = fp.read()
        except Exception:
            return self.handle_error(404, "file %s not found" % filename)
        self.send_response(200)
        #self.send_header("Content-type", "text/html")
        self.end_headers()
        context['args'] = args
        self.wfile.write(bytes(parse_file(data, context),"UTF-8"))


def run_while_true(port=8080, server_class=ThreadingHTTPServer,
                   handler_class=Handler):
    """
    This assumes that keep_running() is a function of no arguments which
    is tested initially and after each request.  If its return value
    is true, the server continues.
    """
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    while True:
        httpd.handle_request()


def parse_file(text, context):
    i = 0
    mode = "html"
    open_index = -1
    while(i < len(text)):
        if mode == "html":
            if text[i] == "<":
                if text[i + 1] == "?":
                    i = i + 1
                    mode = "pyhp"
                    open_index = i + 1
        if mode == "pyhp":
            if text[i] == "?":
                if text[i + 1] == ">":
                    # print text[open_index:i]
                    ret = compile(write_header + text[open_index:i], "<string>", "exec")
                    context['out'] = ""
                    try:
                        exec(ret, context, {})
                    except Exception as E:
                        return str(E)
                    text = text[:open_index - 2] + context['__out'] + text[i + 2:]
                    return parse_file(text, context)
        i = i + 1
    return text


if __name__ == "__main__":
    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 8000
    run_while_true(port)
