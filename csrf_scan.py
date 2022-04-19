from urllib import request
import colorama
from colorama import Fore
import pyfiglet
import re
import sys

colorama.init(autoreset=True)
url = sys.argv[1]

#useragent can be changed as per requirement
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'

Banner = pyfiglet.figlet_format("CSRF Scanner")
print(Fore.LIGHTBLUE_EX + Banner)

def csrf_scan(url):
    print(Fore.LIGHTYELLOW_EX + f"[#] Searching for CSRF tokens on {url} \n")

    #additional headers can be included if required
    req = request.Request(f'{url}', headers={'User-Agent': f'{USER_AGENT}'})
    response = request.urlopen(req)

    #update the list with new keywords
    csrf = ['anticsrf', 'CSRFToken', '__RequestVerificationToken', 'csrfmiddlewaretoken', 'authenticity_token', 'OWASP_CSRFTOKEN', 'anoncsrf', 'csrf_token', '_csrf', '_csrfSecret', '__csrf_magic', 'CSRF', '_token', '_csrf_token','hidden']

    res = str(response.read())
    flag = 0

    #scraping all the forms and input tags
    forms = re.findall(r'<form(.*?)>', res)
    inputs = re.findall(r'<input(.*?)>', res)

    #checking if the tokens are present in the scrapped tags
    for token in csrf:
        for form, inp in ((form, inp) for form in forms for inp in inputs):
            if token in form or token in inp:
                flag = 1
                break

    if flag == 0:
        print(Fore.LIGHTRED_EX + '[-] No CSRF Token present...it is recommended to have one!!')
    elif flag ==1:
        print(Fore.LIGHTGREEN_EX + '[+] CSRF Token(s) present')
   
csrf_scan(url)