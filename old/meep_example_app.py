import meeplib
import traceback
import cgi
import cPickle


def initialize():
    # create a default user
    u = meeplib.User('a Llama', 'box')

    # create a thread (i.e. title for message)
    #t = meeplib.Thread('Test Thread')
    # create a single message
    #m = meeplib.Message('This is my message!', u)
    # save the message in the thread
    #t.add_post(m)



class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])

        username = 'a Llama'

        return ["""<h1>Welcome <i style = "color:red;">Human</i>!</h1><h2>Please Login or create an account.</h2>
<form action='login' method='POST'>
Username:<input type='text' name='username'><br>
Password:<input type='password' name='password'>&nbsp;<br>
<input type='submit' value='Login'></form>

<p>Don't have an account? Create a user <a href='/create_user'>here</a>"""]

    def home_page(self, environ, start_response):
        try:
            meeplib.get_curr_user()
        except NameError:
            meeplib.delete_curr_user()
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)
        username = meeplib.get_curr_user()

        return ["""%s logged in!<p><a href='/m/add_message'>Add a Message</a><p><a href='/create_user'>Create a User</a><p><a href='/logout'>Log out</a><p><a href='/m/list'>Show All Messages</a>""" % (username,)]

    def create_user(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("302 Found", headers)
        return """<form action='add_new_user' method='POST'>
Username: <input type='text' name='username'><br>
Password:<input type='password' name='password'><br>
<input type='submit' value='Create User'></form>"""

    def add_new_user(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        returnStatement = "user added"
        try:
            username = form['username'].value
        except KeyError:
            username = None
        try:
            password = form['password'].value
        except KeyError:
            password = None

        print username
        print password
        # Test whether variable is defined to be None
        if username is None:
            returnStatement = "username was not set. User could not be created"
        if password is None:
            returnStatement = "password was not set. User could not be created"
        else:
            new_user = meeplib.User(username, password)

        

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/'))
        start_response("302 Found", headers)

        return [returnStatement]

    def login(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        returnStatement = "logged in"
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
        # Test whether variable is defined to be None
        if username is not None:
             if password is not None:
                 if meeplib.check_user(username, password) is True:
                     new_user = meeplib.User(username, password)
                     meeplib.set_curr_user(username)
                     k = 'Location'
                     v = '/home_page'
                 else:
                     k = 'Location'
                     v = '/'
                     returnStatement = """<p>Invalid user.  Please try again.</p>"""

             else:      
                 returnStatement = """<p>password was not set. User could not be created</p>"""
        else:
            returnStatement = """<p>username was not set. User could not be created</p>"""

        print """isValidafter: %s """ %(meeplib.check_user(username, password),)

        # set content-type
        headers = [('Content-type', 'text/html')]
       
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"    

    def logout(self, environ, start_response):
        # does nothing
        headers = [('Content-type', 'text/html')]

        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"

    def list_messages(self, environ, start_response):
        messages = meeplib.get_all_threads()
        
        s = []
        if messages:
            for t in messages:
                flag = 0
                for m in t.get_all_posts():
                    s.append('<hr>')
                    if flag == 0: 
                        s.append('<h2>%s</h2>' % (t.title))
                        flag = 1
                    s.append('<p>%s</p>' % (m.post))
                    s.append('<p>Posted by: %s</p>' % (m.author.username))
                    # append the delete message link
                    s.append("""
                    <form action='delete_action' method='POST'>
                    <input name='thread_id' type='hidden' value='%d' />
                    <input name='post_id' type='hidden' value='%d' />
                    <input name='delete' type='submit' value='Delete Message' />
                    </form>
                    """  % (t.id, m.id))
                s.append("""
                <form action='reply' method='POST'>
                <input name='thread_id' type='hidden' value='%d' />
                <input name='reply' type='submit' value='Reply to' />
                </form>
                """ % (t.id))
        else:
            s.append("There are no messages to display.<p>")

        s.append('<hr>')
        s.append("<a href='../../home_page'>Back to the Home Page</a>")
            
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return ["".join(s)]

    def add_message(self, environ, start_response):
        headers = [('Content-type', 'text/html')]

        start_response("200 OK", headers)

        return """<form action='add_message_action' method='POST'>Title: <input type='text' name='title'><br>Message: <input type='text' name='message'><br><input type='submit'></form>"""

    def add_message_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        title = form['title'].value
        message = form['message'].value
        
        username = meeplib.get_curr_user()
        user = meeplib.get_user(username)
        
        new_message = meeplib.Message(message, user)
        t = meeplib.Thread(title)
        t.add_post(new_message)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message added"]

    def delete_message_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        thread_id = int(form['thread_id'].value)
        post_id = int(form['post_id'].value)

        t = meeplib.get_thread(thread_id)
        post = t.get_post(post_id)
        t.delete_post(post)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)

        return["post deleted"]
        
    def reply(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        thread_id = int(form['thread_id'].value)
        t = meeplib.get_thread(thread_id)
        
        s = []
        flag = 0
        for m in t.get_all_posts():
            s.append('<hr>')
            if flag == 0: 
                s.append('<h2>%s</h2>' % (t.title))
                flag = 1
            s.append('<p>%s</p>' % (m.post))
            s.append('<p>Posted by: %s</p>' % (m.author.username))
        s.append('<hr>')
        s.append("""
        <form action='reply_action' method='POST'>
        <input name='thread_id' type='hidden' value='%d' />
        Message: <input type='text' name='post'><br>
        <input type='submit'>
        </form>
        """ % (t.id))
            
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        return ["".join(s)]

    def reply_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        post = form['post'].value

        username = 'a Llama'
        user = meeplib.get_user(username)

        new_message = meeplib.Message(post, user)
        thread_id = int(form['thread_id'].value)
        
        t = meeplib.get_thread(thread_id)
        t.add_post(new_message)
        

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["reply added"]
    
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/home_page': self.home_page,
                      '/create_user': self.create_user,
                      '/add_new_user':self.add_new_user,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/add_message': self.add_message,
                      '/m/add_message_action': self.add_message_action,
                      '/m/delete_action': self.delete_message_action,
                      '/m/reply': self.reply,
                      '/m/reply_action': self.reply_action
                      }

        # see if the URL is in 'call_dict'; if it is, call that function.
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
