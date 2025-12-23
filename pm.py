import argparse
from getpass import getpass
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from utils.dbconfig import dbconfig
from utils.add_entry import addEntry
from utils.retrieve_entry import retrieveEntries
from utils.passwordGenerator import passwordGenerator
from rich import print as printc
import pyperclip
parser=argparse.ArgumentParser(description="Password Manager")
parser.add_argument('option' , help='(a)dd / (e)xtract / (g)enerate')
parser.add_argument("-d","--domain" , help="Site name")
parser.add_argument("-u","--url",help="Site URL")
parser.add_argument("-e","--email",help="Email")
parser.add_argument("-l","--uname",help="Username")
parser.add_argument("--length",help="Length of the password to generate",type=int)
parser.add_argument("-c","--copy",action='store_true',help='Copy password to clipboard')

args=parser.parse_args()

def Authentication():
    maspass=getpass("Enter Master Password: ")
    db=dbconfig()
    cursor=db.cursor()
    query="SELECT * FROM pm.secrets"
    cursor.execute(query)
    result=cursor.fetchall()[0]
    ph=PasswordHasher(
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        salt_len=16
    )
    try:
        ph.verify(result[0],maspass)
        return [maspass,result[1]]
    
    except VerifyMismatchError :
        printc("[red][!] Incorrect master password. Please try again.[/red]")
        return None


 

def main():
    if args.option in ["add" , "a"]:
        if args.domain==None or args.url==None or args.uname==None:
            if args.domain==None:
                printc("[red][!][/red] Site Name (-s) required ")
            if args.url==None:
                printc("[red][!][/red] Site URL (-u) required ")
            if args.uname==None:
                printc("[red][!][/red] Login Username (-l) required ")
            return
        if args.email==None:
            args.email=""
        res=Authentication()
        if res is not None:
            addEntry(res[0],res[1],args.domain,args.url,args.email,args.uname)
    if args.option in ["extract","e"]:
        res=Authentication()
        search={}
        if args.domain is not None:
            search["sitename"]=args.domain
        if args.url is not None:
            search["siteurl"]=args.url
        if args.email is not None:
            search["email"] = args.email
        if args.uname is not None:
            search["username"]=args.uname
        
        if res is not None:
            retrieveEntries(res[0],res[1],search,decryptPassword=args.copy)
        
    if args.option in ["generate","g"]:
        if args.length==None:
            printc("[red][+][/red] Specify Length of the password to generate (--length) ")
            return
        password=passwordGenerator(args.length)
        pyperclip.copy(password)
        printc("[green][+][/green] [bold] Password generated and copied to clipboard ")

if(__name__=="__main__"):
    main()

