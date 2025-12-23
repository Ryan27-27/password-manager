import requests
import hashlib
# HIBP ---> HAVE I BEEN PWNED
HIBP_API = "https://api.pwnedpasswords.com/range/"
def isPasswordPwned(password):
    sha1_hash=hashlib.sha1(password.encode("utf-8")).hexdigest().upper() #HIBP uses hexdecimal in upper case as the password hash
    prefix=sha1_hash[:5]
    suffix=sha1_hash[5:]
    try:
        response=requests.get(
            HIBP_API+prefix, #k-anonymity privacy model uses only 5 char hash
            headers={"User-Agent": "PasswordManager"}, #Requests without a User-Agent may be rejected or throttled     
            timeout=3  
        )
    except requests.exceptions.RequestException as e:
        print(" Unable to check password breach at the moment. Please check your internet connection and try again.")
        return None


    if response.status_code != 200:
        print("Password breach service is temporarily unavailable. Please try again later.")
        return None

    
    for line in response.text.splitlines():
        hash_suffix,count=line.split(":")
        if hash_suffix==suffix:
            return int(count)
    return None




    

