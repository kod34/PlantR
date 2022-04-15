import argparse

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('required named arguments')

requiredNamed.add_argument("-a", "--apk", dest="apk", help="Original APK")
requiredNamed.add_argument("-m", "--mode", dest="mode", help="Injection mode")

args = parser.parse_args()

# Args initiate
apk = args.apk
mode = args.mode
