This is final homeworks 10 and 11 together.
This app uses Django to achieve the similar functionality of Meep,
and uses SQL in implement the login sessions of the app.


###Requirements:

You need the install the following in order for it work correctly:
		-pybbm (http://readthedocs.org/docs/pybbm/en/latest/install.html#requirements)
		-django >= 1.4
		-django-registration >=.8 (http://docs.b-list.org/django-registration/0.8/quickstart.html)
		
Easiest way to install them is to use pip or easy_install:

	pip install pybbm
	pip install django-registration
	pip install django (although it is probably not needed since pybbm will install it too)
	

###How to use:

Once you have those all installed, run terminal and  make sure you are in the root directory of myproject where manage.py is located:
		
	/myproject/
		
Then sync the db for good measure:

	/python manage.py syncdb
	
Then run the server

	/python manage.py runserver
	
Once that is running, go to 127.0.0.1:8000 in a browser

You will need to create a site in order to post messages to the forum, so click login and then the link to create a user at the bottom.

You will be prompted to enter a username and password that you'd like to use, along with an email address to recieve the activiation code.
If you don't want to use your email (I don't blame you), you can just make up a random email using the site mailinator.
If you chose to use mailinator, just use the email address thisisjustatest1234@mailinator.com and access the inbox here:
		http://www.mailinator.com/displayemail.jsp?email=thisisjustatest1234&msgid=17849513
		
Once you recieve the email, click on the link in order to activate and register your account.

From there, just login and enjoy.
	
	