import os
import gnupg
import builtins
# Try to get the original username (not "root") from shell
'''
try:
	user = os.getlogin()
except:
	user = os.environ.get("SUDO_USER")

# Get the uid of the user to be used as the passphrase
uid = os.getuid()
'''

user = builtins.howdy_user
uid = builtins.howdy_uid

os.system('rm -rf /home/'+user+'/.howdy')
gpg = gnupg.GPG(gnupghome='/home/'+user+'/.howdy')

public_keys = gpg.list_keys() 

print(user , uid)
if len(public_keys) == 0 :

	input_data = gpg.gen_key_input(
	    name_email= user+'@local', # Fingerprint
	    passphrase= uid)           # passphrase

	key = gpg.gen_key(input_data)



