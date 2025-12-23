from utils.dbconfig import dbconfig
from utils.passbreachCheck import isPasswordPwned
from getpass import getpass
from argon2 import PasswordHasher
from zxcvbn import zxcvbn
import sys
import os
from rich import print as printc
from rich.console import Console

console=Console()

def genearateDeviceSecret(length=32):
    return os.urandom(length)

def checkConfig():
    db=dbconfig()
    cursor=db.cursor()
    query="SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME='pm'"
    cursor.execute(query)
    result=cursor.fetchall()
    db.close()
    if len(result)!=0 :
        return True
    return False
def reset():
    if not checkConfig():
       printc("[yellow][-][/yellow][bold]No Configuration exists to delete!")
       return
    
    db=dbconfig()
    cursor=db.cursor()
    query="DROP DATABASE pm"
    cursor.execute(query)
    db.commit()
    db.close()

def passwordStrengthCheck(password):
    result=zxcvbn(password)
    if result["score"]>=3:
        printc("[green][+][/green][bold]Strong Password")
    else:
        printc("[red][-][bold]Weak Password[/red]")
        reset()
        sys.exit(0)

def make():
    #check if Database exists
    if checkConfig():
        printc("[red][!][bold]Already Configured! [/red]")
        return
    printc("[green][+]Creating New Config[/green]")

    #Create a Database
    db=dbconfig()
    cursor=db.cursor()
    # the .cursor() method is how you interact with the database to execute SQL queries and fetch results.
    printc("[green][+] Creating New Config [/green]")

    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS pm")
    except Exception as e:
        printc("[red][!] An Error occured while trying to create db[/red]")
        console.print_exception(show_locals=True)
        sys.exit(0)
    printc("[green][+][/green] [bold italic]Database 'pm' created")

    #Create tables;
    query="CREATE TABLE IF NOT EXISTS pm.secrets(masterkey_hash TEXT NOT NULL, device_secret BLOB NOT NULL)"
    res=cursor.execute(query)
    printc("[green][+][/green] [bold italic]Table 'secrets' created")

    query="CREATE TABLE IF NOT EXISTS pm.entries(sitename TEXT NOT NULL , siteurl TEXT NOT NULL, email TEXT , username TEXT, password BLOB NOT NULL, nonce BLOB NOT NULL)"
    res=cursor.execute(query)
    printc("[green][+][/green][bold italic] Table 'entries' created")
    
    #Get Master Password
    mp = ""
    printc("[green][+] A [bold]MASTER PASSWORD[/bold] is the only password you will need to remember in-order to access all your other passwords. " \
    "Choosing a strong [bold]MASTER PASSWORD[/bold] is essential because all your other passwords will be [bold]encrypted[/bold] with a key that is derived from your [bold]MASTER PASSWORD[/bold]. Therefore," \
    "please choose a strong one that has upper and lower case characters, numbers and also special characters. Remember your [bold]MASTER PASSWORD[/bold] " \
    "because it won't be stored anywhere by this program, and you also cannot change it once chosen. [/green]\n")
    while True:
        mp=getpass("Choose a Secure MASTER PASSWORD: ")
        check=isPasswordPwned(mp)
        if check is not None:
            printc(f"[red][!][bold]Password has been breached {check} times.\nUse Another one or use password generator")
            reset()
            sys.exit(1)
        else:
            printc("[green][+][/green]Password has not been breached")
        
        passwordStrengthCheck(mp)
        if(mp==getpass("Re-type: ") and mp!=""):
            break
        printc("[yellow][-] Please try again. [/yellow]")
    
    #Hash the Master password
    ph=PasswordHasher(
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        salt_len=16
    )
    hashed_mp=ph.hash(mp)
    printc("[green][+][/green] [bold]Generated hash of Master Password")
    
    #Generate a device secret
    ds=genearateDeviceSecret()
    printc("[green][+][/green] [bold] Device secret generated")

    query="Insert INTO pm.secrets(masterkey_hash , device_secret) values (%s,%s)"
    val=(hashed_mp,ds)
    cursor.execute(query,val)
    db.commit()

    printc("[green][+][/green] [bold] Added to the database")
    printc("[green][+] [bold]Configuration done! [/green]")

    db.close()

def delete():
    printc("[red][-] Deleting a config clears the device secret and all your entries from the database." \
    " This means you will loose access to all your passwords that you have added into the password manager until now." \
    " Only do this if you truly want to 'destroy' all your entries. This action cannot be undone. [/red]")

    while True:
        opt=input("Are you Sure you want to continue? (Y/N): ")
        if opt.upper()=='Y':
            break
        if opt.upper()=='N' or opt.upper=="":
            sys.exit(0)
        else:
            continue
    printc("[green][-][/green] Deleting Config")

    reset()
    printc("[green][+]Config deleted![/green]")

def remake():
    printc("[green][+]Remaking config[/green]")
    delete()
    make()


if(__name__=="__main__"):
   if len(sys.argv)!=2:
       printc("[bold]Usage: python config.py <make/delete/remake>")
       sys.exit(0)
   if sys.argv[1]=="make":
       make()
   elif sys.argv[1]=="delete":
       delete()
   elif sys.argv[1]=="remake":
       remake()
   else:
       printc("[bold]Usage: python config.py <make/delete/remake>")







