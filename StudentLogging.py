from bs4 import BeautifulSoup as bs 
import requests 

success = False

baseLoginURL = "https://epita-etu.helvetius.net/pegasus/index.php" 
baseNotesURL = "https://epita-etu.helvetius.net/pegasus/index.php?com=extract&job=extract-notes"

def censor(string, censorLength=4):
    return string[:censorLength] + "*" * (len(string) - censorLength)

def get_new_cookie(credentialsPayload):
    getCookieSession = requests.session() 
    response = getCookieSession.post(baseLoginURL, data=credentialsPayload) 
    if verbose: print(f"     used credentials : {censor(credentialsPayload['login'])} / {censor(credentialsPayload['password'], 0)}")
    try:
        newPHPSESSIDCookie = response.request.headers["Cookie"].split("=")[1]
    except:
        if verbose: print("❌ failed to get cookie. please check your credentials.")
        newPHPSESSIDCookie = ""
    return newPHPSESSIDCookie

def check_cookie(cookie):
    if cookie == "":
        return False
    checkCookieSession = requests.session()
    response = checkCookieSession.post(baseLoginURL, cookies={"PHPSESSID": cookie}) 
    if verbose: print(f"    ⏬ got response: {response.status_code}")
    if bs(response.content, "html.parser").find(attrs={"id": "inputLogin"}):
        return False

    return response.status_code == 200


def log(credentialFile, cookieFile, verboseOutput=False):
    global verbose
    verbose = verboseOutput

    if verbose: print("-verbose is enabled-")
    if verbose: print("=== CHRYSAOR - PEGASUS UNOFFICIAL API ===")
    studentName = ""
    PHPSESSIDCookie = ""

    with open(credentialFile, "r") as file:
        data = file.read().split("\n")
        payloadWithCredentials = {
            "login": data[0],
            "password": data[1],
            "job": "auth-user",
            "com": "login"
        }


    with open(cookieFile, "r") as file:
        PHPSESSIDCookie = file.read()
        if verbose: print("📄 reading PHPSESSID cookie from file")

    if verbose: print(" checking cookie...")

    isCookieValid = check_cookie(PHPSESSIDCookie)
    if not isCookieValid:

        success = False
        if verbose: 
            if PHPSESSIDCookie == "": print("❓ no existing PHPSESSID cookie")
            else: print("❌ cookie is not valid. trying to get new cookie...")
            print("*** generating new cookie...")

        PHPSESSIDCookie = get_new_cookie(payloadWithCredentials)
        if verbose: print(f"-> got new PHPSESSID cookie: {censor(PHPSESSIDCookie)}")
        if verbose: print("🔍 checking new cookie...")
        isNewCookieValid = check_cookie(PHPSESSIDCookie)
        if not isNewCookieValid:
            if verbose: print("❌ new cookie is not valid. please check your credentials.")
        else:
            if verbose: print("     ✅ new cookie is valid")
            success = True
        with open(cookieFile, "w") as file:
            file.write(PHPSESSIDCookie)
            if verbose: print(f"    💾🍪 wrote PHPSESSID cookie to file")
    else:
        if verbose: print("     ✅ cookie is valid")
        success = True


    notesData = requests.post(baseNotesURL, cookies={"PHPSESSID": PHPSESSIDCookie})
    soup = bs(notesData.content, "html.parser") 

    try:
        # <td style="width: 494px; "><label>HERAIL               JEAN <span title="err: chemin=/nfs/photos_epi/jean.herail.jpg, chemin_disk=/data/nfs/photos_epi/jean.herail.jpg">--Pas de photo--</span></label></td>
        studentInfos = soup.find("td", style="width: 494px; ").text.split()
        studentName = f"{studentInfos[1]} {studentInfos[0]}"
        if verbose: print(f"👨 connected as {studentName}")
        success = True

    except:
        if verbose: print("❌🛜 failed to connect. please check your credentials.")
        success = False
    
    return {
        "success": success,
        "cookie": PHPSESSIDCookie,
        "name": studentName
    }