PlantR is a tool that generates a custom payload, injects it to an application apk, creates a specific persistence script and starts a metaploit session.  

## Installation  
./install.sh  
## Usage  
usage: plantr.py [-h] [-a APK] [-m MODE]

optional arguments:
  -h, --help            show this help message and exit  
  
required named arguments:  
  -a APK, --apk APK     Original APK  
  -m MODE, --mode MODE  Injection mode  
  
Examples:  
  
For quick embedding by msfvenom:  
&nbsp;&nbsp;&nbsp;&nbsp;python3 plantr.py -a [apk path] -m auto  
  
For manual embedding:  
&nbsp;&nbsp;&nbsp;&nbsp;python3 plantr.py -a [apk path] -m manual  
  
## Notes  
If automatic injection doesn't work, try manual injection. There is no guarantee that either method will work on all apps.  
## Disclaimer
The sole purpose of writing this program was research, its misuse is the responsibility of the user only.
