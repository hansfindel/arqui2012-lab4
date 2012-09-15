import webapp2
import sys
# para Python 2.6 o inferior, utilizamos unittest2
if sys.hexversion < 0x2070000:
    import unittest2 as unittest
else:
    import unittest

import main

class TestMessages(unittest.TestCase):

	def test_assert(self):
		self.assertTrue(True)
	
	def test_get_path_default(self):
		ruta = "files/data.txt"
		path = main.Escribano().get_path()
		self.assertEquals(path, ruta)
	def test_get_path_misma_ruta(self):
		ruta = "files/data.txt"
		path = main.Escribano().get_path(str(ruta))
		self.assertEquals(path, ruta)
	def test_get_path_ruta_distinta(self):
		path = main.Escribano().get_path()
		self.assertNotEquals(path, "otra_ruta")

	def test_leer_file_exists(self):
		exist = main.Escribano().exists_file()
		self.assertTrue(exist) 

	def test_leer_file_dont_exist(self):
		exist = main.Escribano().exists_file("filas/da.tos")
		self.assertTrue(not exist)

	def test_leer_default(self):
		request = webapp2.Request.blank("/")
		response = request.get_response(main.app)
		self.assertTrue(response)

	def test_leer_existente(self):
		path = main.Escribano().get_path()
		request = webapp2.Request.blank("/?path="+str(path))
		response = request.get_response(main.app)
		self.assertTrue(response)


	def test_escribir_json_archivo_inexistente(self):
		path = main.Escribano().get_path()
		request = webapp2.Request.blank("/?files=holo.json")
		request.data = {"author": "yo", "title": "digo", "message": "algo"}
		request.method = "POST"
		request.headers['Content-Type'] = 'application/json'
		request.headers['Accept'] = 'text/plain'
		response = request.get_response(main.app)
		self.assertTrue(response)	

	def test_escribir_json_text_archivo_inexistente(self):
		path = main.Escribano().get_path()
		request = webapp2.Request.blank("/?files=holo.json")
		request.data = "'hola':'holi'"
		request.method = "POST"
		request.headers['Content-Type'] = 'application/json'
		request.headers['Accept'] = 'text/plain'
		response = request.get_response(main.app)
		self.assertTrue(response)	

	def test_escribir_texto_archivo_inexistente(self):
		path = main.Escribano().get_path()
		request = webapp2.Request.blank("/?files=holi.json")
		request.data = "'hola':'holi'"
		request.method = "POST"
		request.headers['Content-Type'] = 'text/html'
		response = request.get_response(main.app)
		self.assertTrue(response)	

	def test_escribir_json_archivo_existente(self):
		path = main.Escribano().get_path()
		request = webapp2.Request.blank("/")
		request.data = {"author": "yo", "title": "digo", "message": "algo"}
		request.method = "POST"
		request.headers['Content-Type'] = 'application/json'
		request.headers['Accept'] = 'text/plain'
		response = request.get_response(main.app)
		self.assertTrue(response)	
	def test_escribir_json_text_archivo_existente(self):
		path = main.Escribano().get_path()
		request = webapp2.Request.blank("/")
		request.data = "hola hola"
		request.method = "POST"
		request.headers['Content-Type'] = 'application/json'
		request.headers['Accept'] = 'text/plain'
		response = request.get_response(main.app)
		self.assertTrue(response)	

	def test_escribir_texto_archivo_existente(self):
		path = main.Escribano().get_path()
		request = webapp2.Request.blank("/")
		request.data = "'hola':'holi'"
		request.method = "POST"
		request.headers['Content-Type'] = 'text/html'
		response = request.get_response(main.app)
		self.assertTrue(response)	
