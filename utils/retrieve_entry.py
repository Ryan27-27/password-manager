from utils.dbconfig import dbconfig
from rich import print as printc
from rich.console import Console
from rich.table import Table
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from utils.add_entry import derive_key
import pyperclip
def decryt_Password(masterKey:bytes,ciphertext:bytes,nonce:bytes):
    aes=AESGCM(masterKey)
    plaintext=aes.decrypt(nonce,ciphertext,None)
    return plaintext.decode()

def retrieveEntries(masterPasswd,deviceSecret,search,decryptPassword=False):
    db=dbconfig()
    cursor=db.cursor()
    query=""
    if len(search)==0:
        query="SELECT * FROM pm.entries"
    else:
        query+="SELECT * FROM pm.entries WHERE "
        for i in search:
            query+=f"{i} = '{search[i]}' AND "
        query=query[:-5]
    cursor.execute(query)
    results=cursor.fetchall()

    if len(results)==0:
        printc("[yellow][-][/yellow] [bold] No results for the search")
        return
    if (decryptPassword and len(results)>1) or (not decryptPassword):
        table=Table(title="Results")
        table.add_column("Site Name")
        table.add_column("Site URL")
        table.add_column("Email")
        table.add_column("Username")
        table.add_column("Password")

        for i in results:
            table.add_row(i[0],i[1],i[2],i[3],"[bold]********")
        console=Console()
        console.print(table)
        return
    if len(results)==1 and decryptPassword:
        masterKey=derive_key(masterPasswd,deviceSecret)
        decrypted=decryt_Password(masterKey,results[0][4],results[0][5])
        pyperclip.copy(decrypted)
        printc("[green][+][/green] [bold black]Password copied to clipboard")
    db.close()
    
