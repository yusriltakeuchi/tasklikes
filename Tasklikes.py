from tasks import Tasklikes
from flask import Flask, request, abort
from getpass import getpass
from apscheduler.schedulers.background import BackgroundScheduler
from colorama import init
from colorama import Fore, Back, Style
import sys
import os
init()

app = Flask(__name__)

@app.route("/callback", methods=['GET']) 
def callback():
    return 'Pinger OK!'

'''
Tasklikes adalah sebuah scripts 
melakukan otomatis likes ke postingan
instagram berdasarkan hastag tertentu yang
dipilih secara acak. Kemudian dia juga akan
menelusuri tiap user yang didapat untuk
di like juga postingannya.

@author: Yusril Rapsanjani
@version: v1.0
'''

YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
RED = Fore.RED


'''
Fungsi ini bertujuan untuk 
menjalankan proses otomatis like.
Diperlukan credentials berupa
username dan password.
'''
def runLikes(username, password):

    #Memanggil class object tasklikes
    tasks = Tasklikes(username, password)
    #Melakukan login untuk mendapatkan session
    tasks.login()

    '''
    Mendapatkan detail mengenai user 
    seperti jumlah Fullname, Follower dan Following
    '''
    print("    " + YELLOW + "=========================")
    tasks.getUsersDetail(username)
    print("    " + YELLOW + "=========================")

    #Mendapatkan random hastag dari data_config.yml
    hastag = tasks.getRandomHastag()

    #Mendapatkan list media berdasarkan hastag terpilih
    media_data = tasks.getMediaByTag(hastag)
    print("    {0}Mendapatkan {1}{2}{0} media dari hastag #{3}".format(YELLOW, BLUE,str(len(media_data)), hastag))

    '''
    Melakukan like ke semua media yang didapat.
    Parameter 'yes' artinya ingin menambahkan
    data username pada tiap postingan yang dilikes
    '''
    tasks.likeAllMediaPost(media_data, "yes", True)
    #Mendapatkan data usernamenya
    username_list = tasks.getUsernameList()

    '''
    Proses ini bertujuan untuk mendapatkan
    list media tiap user yang tersimpan usernamenya,
    kemudian akan melakukan likes sebanyak 12 postingan.
    '''
    if len(username_list) > 0:
        print("    " + YELLOW + "==================================")
        print("    {0}Mendapatkan {1}{2}{0} data username".format(YELLOW, BLUE, str(len(username_list))))
        tasks.LikeAllMediaUser(username_list)

def headers():
    print(" ")
    print("{0}      ------[ {1}Tasklikes {0}]------".format(YELLOW, BLUE))
    print("{0}    {1}Automatic instagram likes hastag".format(YELLOW, BLUE))
    print("{0}    --------------------------------".format(YELLOW))
    print("{0}      Written by Yusril Rapsanjani  ".format(BLUE))
    print("{0}            Version v1.0  ".format(BLUE))
    print("{0}    --------------------------------".format(YELLOW))


'''
Mendeteksi argument
Example format:
python3 Tasklikes --type onetime --username yourusername
'''
def parsingArg():
    types = ""
    username = ""
    password = ""
    for x in range(0, len(sys.argv)):
        if sys.argv[x] == "--type":
            types = sys.argv[x+1]
        elif sys.argv[x] == "--username":
            username = sys.argv[x+1]
        elif sys.argv[x] == '--password':
            password = sys.argv[x+1]

    if username != "" and password == "":
        password = getpass(prompt="    Your Password: ")

    return types, username, password

if __name__ == "__main__":
    headers()
    types, username, password = parsingArg()

    if types == 'onetime':
        runLikes(username, password)

    elif types == 'cron':
        #Create background scheduler object
        sched = BackgroundScheduler(daemon=True)

        sched.add_job(runLikes, 'interval', args=[username, password], minutes=30)
        sched.start()

        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)