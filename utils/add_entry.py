from getpass import getpass
from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import sys
from utils.dbconfig import dbconfig
from utils.passbreachCheck import isPasswordPwned
from rich import print as printc
def derive_key(master_passwd: str, salt:bytes) -> bytes:
    return hash_secret_raw(
        secret=master_passwd.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=Type.ID
    )

def encrypt_passwd(passwd:str, masterKey:bytes)->tuple[bytes,bytes]:
     aesgcm=AESGCM(masterKey)
     nonce=os.urandom(12)

     ciphertext=aesgcm.encrypt(nonce,passwd.encode(),None)
     return nonce, ciphertext


def addEntry(masterPasswd,deviceSecret,sitename,siteurl,email,username):
    #get the password
    passwd=getpass("Enter Password: ")
    check=isPasswordPwned(passwd)
    if check is not None:
        printc(f"[red][!][bold]Password has been breached {check} times.\nUse Another one or use password generator")
        sys.exit(1)
    else:
        printc("[green][+][/green]Password has not been breached")
    
    masterKey=derive_key(masterPasswd,deviceSecret)
    nonce,encrypted=encrypt_passwd(passwd,masterKey)

    #Add to db
    db=dbconfig()
    cursor=db.cursor()
    query="INSERT INTO pm.entries(sitename,siteurl,email,username,password,nonce) values(%s,%s,%s,%s,%s,%s)"
    val=(sitename,siteurl,email,username,encrypted,nonce)
    cursor.execute(query,val)
    db.commit()

    printc("[green][+][/green] [bold] Added Entry ")
    
