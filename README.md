[PHPMYASS [v0.53] "all your dumnb ass auth=config bases are belong to PHPMYASS]

         _/_/_/_/_/    _/  _/_/_/  _/     _/ _/    _/ _/_/_/_/ _/_/_/_/ _/_/_/_/
        _/    _/ _/   _/  _/    _/_/_/ _/_/  _/ _/  _/     _/  _/       _/
       _/_/_/  _/_/_/_/  _/_/_/  _/  _/ _/   _/    _/_/_/ _/    _/_/     _/_/
      _/      _/    _/  _/      _/     _/   _/    _/     _/        _/       _/
     _/      _/    _/  _/      _/     _/   _/    _/     _/ _/_/_/_/ _/_/_/_/

[PHPMYASS | A LESSON IN SERVER MISCONFIGURATION | FIZZLE STICK (Professor)]
[PYTHON]

>> TESTED AGAINST: WINDOWS(XAMPP,UWAMP) and LINUX(XAMPP)

>> workFLOW: discover, inject, validate, report.....  

"what does this do?"....
> this is designed to leverage misconfigured phpmyadmin installations with auth=config.
> the process is agnostic, and can have sexy time with both windows or linux in theory.
> We look for the open page, find some crap we need, clean it up, and then create an PHP shell.
> The current version has added PHP METERPRETER delivery as part of function.

CHANGELOG
- v0.54 - 10/12/2013 - Removed scapy bits / unified the pma detection w nix/win
- v0.53 - 10/10/2013 - Fixed a typo / Added an extensive phpma list from websploit
- v0.52 - 10/02/2013 - Added PHP meterpreter upload function, tested against WIN/NIX.
- v0.51 - 09/15/2013 - Complete re-write to improve everything. Same feature set.
- v0.5  - Initial public github posting

ISSUES
- Report issues to TROLLSOHARD@REBELBAS.ES

TODO
- Improve PHPINFO.PHP detection
- Improve linux effectiveness due to wwwdir permissions
