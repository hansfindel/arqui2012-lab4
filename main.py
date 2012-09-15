import cgi
import webapp2
import requests
import os


class Escribano(webapp2.RequestHandler): 
	def get(self):
		params = str(self.request.query_string)
		path = self.get_path_from_url(params)
		if self.exists_file(path):
			import json
			data = self.leer(path)
			self.response.write(data)
			self.response.headers['Content-Type'] = 'application/json'
		else: 
			self.error(404)
			#self.response.write("Holo... error 404")

	def post(self):
		content_type = cgi.escape(self.request.headers['Content-Type'])
		new_line = cgi.escape(self.request.body)
		#print str(self.request.body)
		path = self.get_path_from_url(str(self.request.query_string))
		if not self.exists_file(path):
			self.crear_bbdd(self.get_path(path))
		self.escribir(new_line, content_type, path)
		self.response.out.write("""
				<html>
					<meta HTTP-EQUIV="REFRESH" content="0; url=http://127.0.0.1:8080">
          		</html>""")


	def get_path_from_url(self, params):
		path = None
		if params == "":
			path = None
		else:
			info = params.split("&")
			for pair in info:
				if path == None:
					key_value = pair.split("=")
					if len(key_value) == 2:
						key = key_value[0]
						value = key_value[1]
						if key == "path":
							path = value
		return path
	def get_path(self, path=None):
		if path != None: 
			ruta = path			
		else:
			ruta = "files/data.txt"
		return ruta
	def exists_file(self, path=None):
		ruta = self.get_path(path)
		if os.path.exists(ruta):
			ans = True
		else:
			ans = False
		return ans
	def leer(self, path=None):
		new_path = self.get_path(path)
		archivo = open(str(new_path),'r')
		data = archivo.read()
		archivo.close()
		return data
	def crear_bbdd(self, path):
		new_file = open(str(path), 'w')
		new_file.write("new")
		new_file.close()
		#print "base de datos creada, path="+str(path)
	def escribir(self, newline, content_type, npath=None):
		if content_type == "application/json":
			self.escribir_json(newline, npath)
		else:
			self.escribir_texto(str(newline), npath)

	def escribir_texto(self, newline, npath=None):
		path = self.get_path(npath)
		archivo = open(str(path), 'r')
		texto = archivo.read()
		new_file = open(str(path), 'w')
		if len(texto) < 5:
			new_file.write("{'messages':['"+newline+"']}")
		else:		
			new_file.write(texto[0:len(texto)-2]+", "+newline+"]}")
		new_file.close()
	def escribir_json(self, newline, npath=None):
		path = self.get_path(npath)
		archivo = open(str(path), 'r')
		texto = archivo.read()
		new_file = open(str(path), 'w')
		if len(texto) < 5:
			new_file.write("{'messages':["+newline+"]}")
		else:		
			new_file.write(texto[0:len(texto)-2]+", "+newline+"]}")
		new_file.close()

class Agregado(webapp2.RequestHandler): 
	def get(self):
		import json
		data = Escribano().leer()
		self.response.write(json.dumps(data))
		self.response.out.write("""
		  <html>
            <body>
              <form action="/agregar" method="post">
                <div><textarea name="body" rows="1" cols="60"></textarea></div>
                <div><input type="submit" value="Agrega algo"></div>
              </form>
            </body>
          </html>""")
	def post(self):
		new_line = cgi.escape(self.request.get('body'))
		#print new_line
		Escribano().escribir(new_line)
		self.response.out.write("""
		<html>
			<meta HTTP-EQUIV="REFRESH" content="0; url=http://127.0.0.1:8080/agregar">
          </html>""")

app = webapp2.WSGIApplication([ ('/', Escribano), ('/agregar', Agregado)], debug=True)  

def main():
	from paste import httpserver 
	httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__': main()
