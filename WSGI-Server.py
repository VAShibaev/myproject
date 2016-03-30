import os
import sys

def my_application(environ, start_response):
    status = '200 OK'
    response_headers = [("Content-Type", "text/html"),
                            ("Connection", "close")]
    result = []
    
    if environ["PATH_INFO"] == "/" or environ["PATH_INFO"] == "/index.html":
        file = open('/Users/stiv/GitHub/myproject/index.html', 'rb')        
        for line in file:
            result.append(line)
        file.close()


    if environ["PATH_INFO"] == "/about/aboutme.html":
        file = open('/Users/stiv/GitHub/myproject/about/aboutme.html', 'rb')
        for line in file:
            result.append(line)
        file.close()

    start_response(status, response_headers)
    return result




class my_middleware(object):
    def __init__(self, my_application):
        self.app = my_application

    def __call__(self, environ, start_response):
        top_position = -1
        top_str = "\t\t<div class='top'>Middleware TOP</div>\n".encode()
        
        bottom_position = -1
        bottom_str = "\t\t<div class='botton'>Middleware BOTTOM</div>\n".encode()
        
        response = self.app(environ, start_response)
        for line in response:
            string = line.decode()
            if "<body>" in string :
                top_position = response.index(line)
            if "</body>" in string :
                bottom_position = response.index(line)

        response = response[:top_position+1] + [top_str] + \
                   response[top_position+1: bottom_position] + [bottom_str] +\
                   response[bottom_position:]
        
        return response




my_application = my_middleware(my_application)
    



if __name__ == '__main__':
    from paste import reloader
    from paste.httpserver import serve

    reloader.install()
    serve(my_application, host='localhost', port=8000)

    
    
        
