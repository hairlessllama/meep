import meeplib
import traceback
import cgi
import cPickle
import meepcookie
import Cookie
import TinyHTTPProxy



from jinja2 import Environment, FileSystemLoader

def initialize():
	meeplib.load()
	# create a default user
	
	u = meeplib.User('a Llama','sheep')
	# create a thread (i.e. title for message)
	
	t = meeplib.Thread('This is a Test Thread')
	
	# create a single message
	m = meeplib.Message('This is a lame test message.', u)
	
	# save the message in the thread
	t.add_post(m)


env = Environment(loader=FileSystemLoader('templates'))

def render_page(filename, **variables):
	template = env.get_template(filename)
	x = template.render(**variables)
	return str(x)

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def index(self, environ, start_response):
		start_response("200 OK", [('Content-type', 'text/html')])
		# get cookie if there is one
		try:
			cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
			username = cookie["username"].value
			print "Username is %s" % username
		except:
			print "The session cookie has not been set yet, defaulting username."
			username = ''
		user = meeplib.get_user(username)
		if user is None:
			return [render_page('login.html')]
		elif user is not None:
			return [render_page('index.html', username = username)]

    def create_user(self, environ, start_response):
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
        except:
            username = ''
        
        user = meeplib.get_user(username)
        if user is not None:
            headers = [('Content-type', 'text/html')]
			
            headers.append(('Location', '/'))
			
            start_response("302 Found", headers)
			
            return ["Already logged in. Must logout to create a user."]

        headers = [('Content-type', 'text/html')]

        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        try:
            username = form['username'].value
        except KeyError:
            username = ''

			
        try:
            password = form['password'].value
        except KeyError:
            password = ''

        s=[]

        #if we have username and password
        if username != '':
            user = meeplib.get_user(username)
            # user already exists
            if user is not None:
                s.append('''User creation has failed, miserably. <br>
                    Your lack of creativity has resulted in an already existing username. <br>
					Please be more creative and create a different username.<p>''')
            # user doesn't exist but password is fucked
            elif password == '':
                s.append('''User was not created. <br>
                    Must input a password to use.<p>''')
            else:
                u = meeplib.User(username, password)
                meeplib.save()
                # redirect it back to '/'
                k = 'Location'
                v = '/'
                headers.append((k, v))
                cookie_name, cookie_val = meepcookie.make_set_cookie_header('username',username)
                headers.append((cookie_name, cookie_val))

        start_response('302 Found', headers)

        s.append(render_page("create_user.html", username=username))
        return [''.join(s)]

    def login(self, environ, start_response):
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
        except:
            username = ''

        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        returnStatement = "Logged In"
        try:
            username = form['username'].value
        except KeyError:
            username = None
        try:
            password = form['password'].value
        except KeyError:
            password = None
        k = 'Location'
        v = '/'
        headers = [('Content-type', 'text/html')]

        # Check to see if defined as None
        if username is not None:
             if password is not None:
                 if meeplib.check_user(username, password) is True:
                     new_user = meeplib.User(username, password)
                     meeplib.set_curr_user(username)
					 
                     #set the cookie to the username
                     cookie_name, cookie_val = meepcookie.make_set_cookie_header('username',username)
                     headers.append((cookie_name, cookie_val))
                 else:
                     returnStatement = """<p>You entered a Higgs boson user. You do not exist(yet). Please try again.</p>"""

             else:      
                 returnStatement = """<p>Password was not set. User was not created.</p>"""
        else:
            returnStatement = """<p>Username was not set. User was not created</p>"""

        print """isValidafter: %s """ %(meeplib.check_user(username, password),)

       
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "The content is a Higgs boson."    

    def logout(self, environ, start_response):
        headers = [('Content-type', 'text/html')]

        #redirects to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        cookie_name,cookie_value = meepcookie.make_set_cookie_header('username','')
        headers.append((cookie_name, cookie_value))
        
        start_response('302 Found', headers)
        
        return "The content is a Higgs boson."   

    def list_messages(self, environ, start_response):
        threads = meeplib.get_all_threads()
        
        # get cookie
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
        except:
            username = ''
        
        user = meeplib.get_user(username)
        s = []
		
        if threads:
            s.append(render_page("list_messages.html", threads=threads, user=user))
        else:
            s.append("There are no threads to display.<p>")

        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)

        return ["".join(s)]

    def add_message(self, environ, start_response):
        #get cookie
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
            print "Username is %s" % username
        except:
            username = ''
        
        user = meeplib.get_user(username)
        if user is None:
            headers = [('Content-type', 'text/html')]
            headers.append(('Location', '/'))
            start_response("302 Found", headers)
            return ["Dude, login first if you want to use this feature."]
        headers = [('Content-type', 'text/html')]

        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        try:
            title = form['title'].value
        except KeyError:
            title = ''
        try:
            message = form ['message'].value
        except KeyError:
            message = ''

        s = []

        #check to see if title and message are not empty
        if title == '' and message == '':
            pass
			
        elif title == '' and message != '':
            s.append("The title is empty.<p>")
			
        elif title != '' and message == '':
            s.append("The message is empty. <p>")
			
        elif title != '' and message != '':
            new_message = meeplib.Message(message, user)
            t = meeplib.Thread(title)
            t.add_post(new_message)
            meeplib.save()
            headers.append(('Location','/m/list'))
            
        start_response("302 Found", headers)
        s.append(render_page("add_message.html", title=title, message=message))

        return ["".join(s)]

		

    def delete_message_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        thread_id = int(form['thread_id'].value)
        post_id = int(form['post_id'].value)

        t = meeplib.get_thread(thread_id)
        post = t.get_post(post_id)
        t.delete_post(post)

        meeplib.save()
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)

        return["Post was deleted."]
        
    def reply(self, environ, start_response):
        # get cookie
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
        except:
            username = ''

        
        user = meeplib.get_user(username)
        if user is None:
            headers = [('Content-type', 'text/html')]
            headers.append(('Location', '/'))
            start_response("302 Found", headers)
            return ["You must be logged in to use that feature."]

        headers = [('Content-type', 'text/html')]

        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
		
        thread_id = int(form['thread_id'].value)
        t = meeplib.get_thread(thread_id)
        s = []

        try:
            post = form['post'].value
        except KeyError:
            post = ''

        #check to make sure post is not empty
        if post != '':
            new_message = meeplib.Message(post, user)
            t.add_post(new_message)
            meeplib.save()
            headers.append(('Location','/m/list'))

        start_response("302 Found", headers)
        s.append(render_page("reply.html", thread=t))
		
        return ["".join(s)]


    
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/create_user': self.create_user,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/add_message': self.add_message,
                      '/m/delete_action': self.delete_message_action,
                      '/m/reply': self.reply,
                      }

        # check to see if the URL is in 'call_dict' and call that function if it is.
        url = environ['PATH_INFO']
        fn = call_dict.get(url)

        if fn is None:
            start_response("404 Not Found", [('Content-type', 'text/html')])
            return ["Page not found."]

        try:
            return fn(environ, start_response)
        except:
            tb = traceback.format_exc()
            x = "<h1>Error!</h1><pre>%s</pre>" % (tb,)

            status = '500 Internal Server Error'
            start_response(status, [('Content-type', 'text/html')])
            return [x]
