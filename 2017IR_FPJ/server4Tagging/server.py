from urllib.parse import urlparse
import http.server
import socketserver

PORT = 8010

blog_list = open('blog_list_2.csv').readlines()

class myHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('tmp', 'r+') as fp:
                index = int(fp.readline().strip())
                c = open('index.html').read().replace('{{index}}', blog_list[index].split(',')[0]).replace('{{url}}', blog_list[index].split(',')[-1].strip())
                self.wfile.write(c.encode('utf8'))
                fp.seek(0, 0)
                index += 1
                if index >= len(blog_list):
                    index = 0
                fp.write(f'{index}\n')
        elif self.path.startswith('/res'):
            parm = self.path.split('?', 1)[-1].split('=')
            open(f"data/{parm[0]}", "a").write(f"{parm[1]}\n")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        elif self.path.startswith('/success'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(open('success.html').read().encode('utf8'))
        elif self.path.startswith('/sres'):
            parm = self.path.split('?', 1)[-1].split('=')[-1]
            print(type(parm))
            open('maillist.txt', 'a').write(f"{parm}\n")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(open('success_res.html').read().encode('utf8'))
        else:
            self.send_response(404)
        return

#Handler = http.server.SimpleHTTPRequestHandler
Handler = myHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
