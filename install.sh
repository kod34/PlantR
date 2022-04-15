#!/bin/bash

sudo apt install metasploit-framework zenity -y

wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool
wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.6.1.jar
mv apktool_2.6.1.jar apktool.jar
chmod +x apktool.jar apktool
sudo mv apktool apktool.jar /usr/local/bin
