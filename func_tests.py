import sys
import unittest
import os
import main
import webapp2
import json

class FunctionalTests(unittest.TestCase):

    def setUp(self):
        import tempfile
        self.old_dir = os.path.abspath(os.curdir) # save old directory
        self.cwd = tempfile.mkdtemp() # new current working directory
        os.chdir(self.cwd)
        
    def tearDown(self):
        import shutil
        os.chdir(self.old_dir)      # restore working directory
        shutil.rmtree(self.cwd)     # delete temp directory
    
    def test_post_con_texto(self):
        request = webapp2.Request.blank('/?path=datos.json')
        request.method = 'POST'
        request.headers['Content-Type'] = 'application/text'
        body = 'prueba'
        request.body = body
        r = request.get_response(main.app)
        request2 = webapp2.Request.blank('/?path=datos.json')
        request2.method = 'GET'
        response = request2.get_response(main.app)
        datos = response.body
        self.assertTrue(datos.index(body) > 0)
        
    def test_post_con_json(self):
        request = webapp2.Request.blank('/?path=datos.json')
        request.method = 'POST'
        request.headers['Content-Type'] = 'application/json'
        data = {"saludo":"hola"}
        request.data = data
        request.get_response(main.app)

        request2 = webapp2.Request.blank('/?path=datos.json')
        request2.method = 'GET'
        response2 = request2.get_response(main.app)
        datos = response2.body
        info = datos[1:-1]
        self.assertTrue(datos.index(info) > 0 )
        
if __name__ == '__main__':
    unittest.main()