       _/_/_/_/_/    _/  _/_/_/  _/     _/ _/    _/ _/_/_/_/ _/_/_/_/ _/_/_/_/
      _/   _/ _/    _/  _/   _/ _/_/ _/_/  _/ _/  _/     _/  _/       _/
     _/_/_/  _/_/_/_/  _/_/_/  _/  _/ _/   _/    _/_/_/ _/    _/_/     _/_/
    _/      _/    _/  _/      _/     _/   _/    _/     _/        _/       _/
   _/      _/    _/  _/      _/     _/   _/    _/     _/ _/_/_/_/ _/_/_/_/

 v0.5
 PHPMYASS | A LESSON IN SERVER MISCONFIGURATION | FIZZLE STICK (Professor)
 TESTED AGAINST: WINDOWS W/ UWAMP, XAMPP
 workFLOW: discover, inject, validate, report.....  
 "what does this do?"....
 - this is designed to leverage misconfigured phpmyadmin installations with auth=config.
 - the process is agnostic, and can have sexy time with both windows or linux in theory.
 - We look for the open page, find some crap we need, clean it up, and then create an PHP shell.
 - currently the result is an upload shell.
