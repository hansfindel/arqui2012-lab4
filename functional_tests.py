import sys
import unittest
import os
import main
import webapp2
import json

class FunctionalTests(unittest.TestCase):
#agregando los test con el setUp y tearDown
    def setUp(self):
        import tempfile
        self.old_dir = os.path.abspath(os.curdir) # save old directory
        self.cwd = tempfile.mkdtemp() # new current working directory
        os.chdir(self.cwd)
        
    def tearDown(self):
        import shutil
        os.chdir(self.old_dir)      # restore working directory
        shutil.rmtree(self.cwd)     # delete temp directory
    
    def test_get_sin_db_ftest(self):
        request = webapp2.Request.blank('/')
        request.method = 'GET'
        response = request.get_response(main.app)      
        self.assertEqual(response.status_int, 404)
        
    def test_get_con_db_ftest(self):
        with open('datos.json', 'w') as writer:
            writer.write(json.dumps('{"mensajes":[]}'))
        request = webapp2.Request.blank('/?path=datos.json')
        request.method = 'GET'
        response = request.get_response(main.app)      
        self.assertEqual(response.status_int, 200)
    
    def test_post_text_sin_db_ftest(self):
        request = webapp2.Request.blank('/?path=holo.json')
        request.method = 'POST'
        request.headers['Content-Type'] = 'application/text'
        request.body = 'no hay db!'
        response = request.get_response(main.app)
        self.assertEqual(response.status_int, 200)
        
    def test_post_text_con_db_ftest(self):
        with open('datos.json', 'w') as writer:
            writer.write(json.dumps('{"mensajes":[]}'))
        request = webapp2.Request.blank('/?path=datos.json')
        request.method = 'POST'
        request.headers['Content-Type'] = 'application/text'
        request.body = 'hola'
        response =request.get_response(main.app)
        self.assertEqual(response.status_int, 200)
        
    def test_post_json_sin_db_ftest(self):
        request = webapp2.Request.blank('/?path=algo_nuevo.json')
        request.method = 'POST'
        request.headers['Content-Type'] = 'application/json'
        request.data = {"saludo":"holo"}
        response =request.get_response(main.app)
        self.assertEqual(response.status_int, 200)
        
    def test_post_json_con_db_ftest(self):
        with open('datos.json', 'w') as writer:
            writer.write(json.dumps('{"mensajes":[]}'))
        request = webapp2.Request.blank('/?path=datos.json')
        request.method = 'POST'
        request.headers['Content-Type'] = 'application/json'
        request.body = json.dumps('{"hola":"holo"}')
        response =request.get_response(main.app)
        self.assertEqual(response.status_int, 200)
    

        
if __name__ == '__main__':
    unittest.main()