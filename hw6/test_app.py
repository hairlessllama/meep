import unittest
import meep_example_app
import urllib
import sys
import os.path
cwd = os.path.dirname(__file__)
importdir = os.path.abspath(os.path.join(cwd, '../'))
if importdir not in sys.path:
    sys.path.append(importdir)
import meep_example_app

class TestApp(unittest.TestCase):
    def setUp(self):
		meep_example_app.initialize()
		app = meep_example_app.MeepExampleApp()
		self.app = app

    def test_index_no_auth(self):
		# make a faux dict
		environ = {} 
		environ['PATH_INFO'] = '/'

		def faux_start_response(status, headers):
			assert status == '200 OK'
			assert ('Content-type', 'text/html') in headers

		data = self.app(environ, faux_start_response)
		assert 'Login' in data[0]
		assert 'here' in data[0]

	def test_index_with_auth(self):
		environ = {}                   
		environ['PATH_INFO'] = '/'
		environ['HTTP_COOKIE'] = "username=poop"

		def faux_start_response(status, headers):
			assert status == '200 OK'
			assert ('Content-type', 'text/html') in headers

		data = self.app(environ, faux_start_response)
		print data[0]
		assert 'Create Message' in data[0]
		assert 'Display Messages' in data[0]

	def test_thread_list(self):
		environ = {}                    
		environ['PATH_INFO'] = '/m/list'

		def faux_start_response(status, headers):
			assert status == '200 OK'
			assert ('Content-type', 'text/html') in headers

		data = self.app(environ, faux_start_response)
		assert 'Back to Main Page' in data[0]

	def test_create_user(self):
		environ = {}                    
		environ['PATH_INFO'] = '/create_user'
		environ['wsgi.input'] = ''

		def faux_start_response(status, headers):
			assert status == '302 Found'
			assert ('Content-type', 'text/html') in headers

        data = self.app(environ, faux_start_response)
		assert 'Username: ' in data[0]
		assert 'Password:' in data[0]

	def test_create_user_action(self):
		environ = {}                  
		environ['PATH_INFO'] = '/create_user'
		environ['wsgi.input'] = ''

		form_dict = {}
		form_dict['username'] = "bear"
		form_dict['password'] = "claw"
		environ['QUERY_STRING'] = urllib.urlencode(form_dict)

	def test_create_thread(self):
		environ = {}                   
		environ['PATH_INFO'] = '/m/add_message'
		environ['wsgi.input'] = ''
		environ['HTTP_COOKIE'] = "username=poop"

		def faux_start_response(status, headers):
			assert status == '302 Found'
			assert ('Content-type', 'text/html') in headers

		data = self.app(environ, faux_start_response)
		print data
		assert 'Title: ' in data[0]
		assert 'Message: ' in data[0]

	def test_create_thread_action(self):
		environ = {}                
		environ['PATH_INFO'] = '/m/add_message'
		environ['wsgi.input'] = ''
		environ['HTTP_COOKIE'] = "username=goat"

		form_dict = {}
		form_dict['title'] = "title"
		form_dict['message'] = "message"
		environ['QUERY_STRING'] = urllib.urlencode(form_dict)

	def test_reply(self):
		environ = {}                  
		environ['PATH_INFO'] = '/m/reply'
		environ['wsgi.input'] = ''
		environ['HTTP_COOKIE'] = "username=poop"

		form_dict = {}
		form_dict['thread_id'] = meeplib.get_next_thread_id()
		environ['QUERY_STRING'] = urllib.urlencode(form_dict)

		def faux_start_response(status, headers):
			assert status == '302 Found'
			assert ('Content-type', 'text/html') in headers

		data = self.app(environ, faux_start_response)
		print data
		assert "Message:" in data[0]

	def test_reply_action(self):
		environ = {}                   
		environ['PATH_INFO'] = '/m/reply'
		environ['wsgi.input'] = ''
		environ['HTTP_COOKIE'] = "username=test"

		form_dict = {}
		form_dict['thread_id'] = 1
		form_dict['post'] = "replyingtest"
		environ['QUERY_STRING'] = urllib.urlencode(form_dict)


	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()