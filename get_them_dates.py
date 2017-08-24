import robobrowser
import re

import itertools
import pynder

NUM_LOOPS = 100
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19"
FB_AUTH = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"


def get_access_token(email, password):
    s = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="lxml")
    s.open(FB_AUTH)
    ##submit login form##
    f = s.get_form()
    f["pass"] = password
    f["email"] = email
    s.submit_form(f)
    ##click the 'ok' button on the dialog informing you that you have already authenticated with the Tinder app##
    f = s.get_form()
    s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])
    ##get access token from the html response##
    access_token = re.search(r"access_token=([\w\d]+)", s.response.content.decode()).groups()[0]

    return access_token


def main():

	# get input from other file
	f = open('variables.txt','r')
	FBID     = f.readline().replace('\n','')
	email    = f.readline().replace('\n','')
	password = f.readline().replace('\n','')

	access_token = get_access_token(email, password)
	session = pynder.Session(facebook_id=FBID, facebook_token=access_token)
	users = session.nearby_users()
	hoes = itertools.islice(users, NUM_LOOPS) 
#	print 'Num nearby users: {}'.format(users.size())

#	matches = session.matches()
#	print 'Current number of matches: {}'.format(matches)

	print "Sequence Initializing"
#	print len(list(hoes)) 

	i=0
	for hoe in hoes:
		wantsToBang = hoe.like()
		print '{} #{}'.format(wantsToBang, i)
		i+=1


#		if wantsToBang:
#			print hoe.name
#			print hoe.age
#			print hoe.ping_time
#			print hoe.distance_km

if __name__ == "__main__": main()
