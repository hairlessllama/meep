import urllib2
import json
import pprint

# Make sure you type press Ctrl+C after a few seconds, because this may loop foor a while


# This example request includes an optional API key which you will need to
# remove or replace with your own key.
# Read more about why it's useful to have an API key.
# The request also includes the userip parameter which provides the end
# user's IP address. Doing so will help distinguish this legitimate
# server-side traffic from traffic which doesn't come from an end-user.
z=1
num_queries = 10*4 
url = ('https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="C.+Titus+Brown"+site:www.cse.msu.edu&rsz=8&key=AIzaSyBrSXCL8WHXPrgLhmgwMYo6no-od8VLsbo&userip=USERS-IP-ADDRESS')


request = urllib2.Request(
    url, None, {'Referer': 'www.msu.edu'})
response = urllib2.urlopen(request)

# Process the JSON string.
results = json.load(response)
# now have some fun with the results...

#for i in results.items:print i

x= results[u'responseData'][u'results']
for i in x:
    print i['title'] + ": " + i['url'] + ": " + i['content']
    z= z+1
    print 'this is z: ', z


#This is an attempt to have the google search api show more than 8 results, but I am not quite sure if it actually does or not haha.
##for start in range(0, num_queries, 4):
##    
##    request = urllib2.Request(
##        url, None, )
##    response = urllib2.urlopen(request)
##
##    # Process the JSON string.
##    results = json.load(response)
##    # now have some fun with the results...
##
##    #for i in results.items:print i
##    pprint.PrettyPrinter(indent=0).pprint(results[u'responseData'][u'results'])
##    z=z+1
##    print "z is:" , z



##    x= results[u'responseData'][u'results']
##    for i in x:
##        print i['title'] + ": " + i['url'] + ": " + i['content']

#pprint.PrettyPrinter(indent=0).pprint(x[]['title'])

#pprint.PrettyPrinter(indent=0).pprint(results[u'responseData'][u'results'])
                                      
