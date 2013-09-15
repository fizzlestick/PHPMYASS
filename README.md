[PHPMYASS [v0.5] GITHUB RELEASE]

         _/_/_/_/_/    _/  _/_/_/  _/     _/ _/    _/ _/_/_/_/ _/_/_/_/ _/_/_/_/
        _/    _/ _/   _/  _/    _/_/_/ _/_/  _/ _/  _/     _/  _/       _/
       _/_/_/  _/_/_/_/  _/_/_/  _/  _/ _/   _/    _/_/_/ _/    _/_/     _/_/
      _/      _/    _/  _/      _/     _/   _/    _/     _/        _/       _/
     _/      _/    _/  _/      _/     _/   _/    _/     _/ _/_/_/_/ _/_/_/_/

[PHPMYASS | A LESSON IN SERVER MISCONFIGURATION | FIZZLE STICK (Professor)]
[PYTHON]

>> TESTED AGAINST: WINDOWS with UwAMP, and XAMPP

>> workFLOW: discover, inject, validate, report.....  

"what does this do?"....
> this is designed to leverage misconfigured phpmyadmin installations with auth=config.
> the process is agnostic, and can have sexy time with both windows or linux in theory.
> We look for the open page, find some crap we need, clean it up, and then create an PHP shell.
> currently the result is an upload shell.

CHANGELOG
- v0.51 - 9/15/2013 - Complete re-write to improve everything. Same feature set.
- v0.5  - Initial public github posting

ISSUES
- Report issues to TROLLSOHARD@REBELBAS.ES

TODO
- I have a couple ideas.. maybe
 #1) add PHP meterpreter stuffs
 #2) add TOR for testing
 #3) add pre_replace vuln from waraxe (I can't get this to repro currently in xlab, even though I did before. ;(
 #4) more interaction with target variables such as wwwroot and the like
