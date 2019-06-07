import requests
import sys
import random
import time
import json
import re
import yaml
from colorama import init
from colorama import Fore, Back, Style

class Tasklikes:
    
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    RED = Fore.RED

    BASE_URL = "https://www.instagram.com"
    IBASE_URL = "https://i.instagram.com"

    ENDPOINT_LOGIN = BASE_URL + "/accounts/login/ajax/"

    ENDPOINT_USERS = IBASE_URL + "/api/v1/users/%s/info/"
    ENDPOINT_API_USERS = BASE_URL + "/%s/?__a=1"

    ENDPOINT_TAG = BASE_URL + "/explore/tags/%s/?__a=1"

    ENDPOINT_LIKES = BASE_URL + "/web/likes/%s/like/"
    ENDPOINT_COMMENT = BASE_URL + "/web/comments/%s/add/"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.status_login = False
        self.user_id = ""
        self.username_list = []

    '''
    Parsing CSRF pada 
    saat proses login untuk 
    disimpan ke session
    ''' 
    def parsingCSRF(self, content):
        return re.search('(?<="csrf_token":")\w+', content).group(0)

    '''
    Mendapatkan detail profile seperti
    fullname, follower, following
    '''
    def getUsersDetail(self, username):
        url_info = self.BASE_URL + "/" + username
        info = self.session.get(url_info)
        json_info = json.loads(
            re.search(
                "window._sharedData = (.*?);</script>", info.text, re.DOTALL
            ).group(1))

        self.session.headers.update({"X-CSRFToken": json_info['config']['csrf_token']})

        print("    {0}Fullname: {1}{2}".format(self.YELLOW, self.BLUE, json_info['config']['viewer']['full_name']))
        print("    {0}Follower: {1}{2}".format(self.YELLOW, self.BLUE, str(json_info['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count'])))
        print("    {0}Following: {1}{2}".format(self.YELLOW, self.BLUE, str(json_info['entry_data']['ProfilePage'][0]['graphql']['user']['edge_follow']['count'])))

    '''
    Mendapatkan list media
    berdasarkan hastag tertentu
    '''
    def getMediaByTag(self, tag):
        if self.status_login:
            url_tag = self.ENDPOINT_TAG % (tag)
        
            try:
                r = self.session.get(url_tag)
                media_data = json.loads(r.text)
               
                media_top = list(
                    media_data["graphql"]["hashtag"]["edge_hashtag_to_top_posts"][
                        "edges"]
                )

                self.media_tag = []
                for med in media_top:
                    self.media_tag.append(med)

                media = list(
                    media_data["graphql"]["hashtag"]["edge_hashtag_to_media"][
                        "edges"
                ])
                for med in media:
                    self.media_tag.append(med)
            except:
                self.media_tag = []

        return self.media_tag

    '''
    Mendapatkan username berdasarkan
    dari user_id
    '''
    def getUsernameById(self, user_id):
        if self.status_login:
            try:
                url_user = self.ENDPOINT_USERS % (user_id)
                data = requests.get(url_user)
               
                profile = json.loads(data.text)
              
                if profile['user']['is_private'] == False:
                    return profile['user']['username']
                else:
                    return 'null'
            except:
                return 'null'

    '''
    Mendapatkan data username list
    '''
    def getUsernameList(self):
        return self.username_list;

    '''
    Fungsi untuk like media berdasarkan
    media_id tertentu
    ''' 
    def likeMedia(self, media_id):
        if self.status_login:
            url_likes = self.ENDPOINT_LIKES % (media_id)
            try:
                like = self.session.post(url_likes)
                
                response = json.loads(like.text)
               
                if response['status'] == 'ok':
                    status = '{0}Like Media: [{2}] => {1} Success'.format(self.YELLOW, self.BLUE, media_id)
                else:
                    status = '{0}Like Media: [{2}] => {1} Failed'.format(self.YELLOW, self.RED, media_id)
                    
            except:
                status = '{0}Like Media: [{2}] => {1} Failed'.format(self.YELLOW, self.RED, media_id)

        return status, like.text

    '''
    Sebuah fungsi yang menjadi inti dari program.
    Dia akan melakukan looping ke semua media yang
    tersedia, kemudian melakukan likes.
    Jika appendUsernamenya 'yes' maka data username list
    akan dibuat. Jika showOwner True, maka akan menampilkan
    siapa pemilik postingan tersebut.
    '''
    def likeAllMediaPost(self, media_data, appendUsername, showOwner):
        count = 0
        
        self.username_list = []
        for x in range(0, len(media_data)):
            count += 1

            media_id = media_data[x]['node']['id']
            media_owner = self.getUsernameById(media_data[x]['node']['owner']['id'])
            
            #Append username to data username list
            if appendUsername == "yes":
                if media_owner != 'null':
                    self.username_list.append(media_owner)

            '''
            Bagian ini memastikan jika ada error
            saat like media, maka dia akan mengulangi
            loopingnya lagi
            '''
            while True:
                status, rawresponse = self.likeMedia(media_id)
                if 'Please wait a few minutes before you try again.' in str(rawresponse):
                    print("    {0}[{1}{2}{0}/{1}{3}{0}] Session likes reached, please wait 60 seconds.".format(self.YELLOW, self.BLUE, str(count), str(len(media_data))))
                    time.sleep(60)

                    #Jika error, dia ulang looping lagi
                    continue
                else:
                    output = "    {0}[{1}{2}{0}/{1}{3}{0}] {4} ".format(self.YELLOW, self.BLUE, str(count), str(len(media_data)), str(status))
                    if showOwner:
                        output += "{0}- Owner: {1}{2}".format(self.YELLOW, self.BLUE, media_owner)
                    print(output)

                    #Jika gaada error, dia lanjut
                    break
                    # comment = self.getRandomComment()
                    # status = self.commentMedia(media_id, comment)
                    # print("{0}     - Comment: {1}{2}".format(self.YELLOW, self.BLUE, comment))

    '''
    Melakukan like ke semua postingan 
    pada username tertentu. Disini akan melakukan
    looping ke semua username
    '''
    def LikeAllMediaUser(self, username_list):
        count = 0
        for username in username_list:
            count += 1
            
            #Jika user sudah berhasil login
            if self.status_login:
                try:
                    print("    " + self.YELLOW + "==================================")
                    
                    url_profile = self.ENDPOINT_API_USERS % (username)
                    data = self.session.get(url_profile)
                    profile = json.loads(data.text)

                    media_list = profile['graphql']['user']['edge_owner_to_timeline_media']['edges']
                    print("    {0}[{1}{2}{0}/{1}{3}{0}]".format(self.YELLOW, self.BLUE, str(count), str(len(username_list))) + "{0} Mencoba melakukan like ke {1}{2} {0}media dari {1}{3}".format(self.YELLOW, self.BLUE, str(len(media_list)), username))

                    '''
                    Melakukan like ke semua media yang didapat.
                    Parameter 'no' artinya tidak ingin menambahkan
                    data username pada tiap postingan yang dilikes
                    '''                
                    self.likeAllMediaPost(media_list, "no", False)
                except:
                    continue

    '''
    Fungsi untuk auto comment ke setiap
    media yang dikunjungi. Kadang kena 
    bad requests 403, jadi belum terlalu
    rekomended dipakai
    '''
    def commentMedia(self, media_id, comment_text):
        if self.status_login:
            url_comment = self.ENDPOINT_COMMENT % (media_id)
            comment_post = {"comment_text": comment_text}
            try:
                comment = self.session.post(url_comment, data=comment_post)
                print(comment)
                if comment.status_code == 200:
                    status = True
                else:
                    status = False
            except:
                status = False

        return status

    '''
    Set default headers untuk session
    '''
    def setDefaultHeaders(self):
        self.session.headers.update({
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Host": "www.instagram.com",
            "Origin": "https://www.instagram.com",
            "Referer": "https://www.instagram.com/",
            "User-Agent": self.getUsersAgents(),
            "X-Instagram-AJAX": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
        })

    '''
    Proses login ke instagram, kemudian
    akan mengambil CSRF tokennya untuk 
    disimpan ke session
    '''
    def login(self):
        #Set default headers
        self.setDefaultHeaders()

        #Data yang akan dikirim untuk login
        self.login_post = {
            "username": self.username,
            "password": self.password
        }

        #Proses pengambilan CSRF Token
        r = self.session.get(self.BASE_URL)
        self.session.headers.update({"X-CSRFToken": self.parsingCSRF(r.text)})

        print("    {0}Mencoba login sebagai {1}{2}".format(self.YELLOW, self.BLUE, self.username))
        time.sleep(5 * random.random())

        #Proses requests login
        login = self.session.post(
            self.ENDPOINT_LOGIN, data=self.login_post, allow_redirects=True)
        loginResponse = login.json()


        '''
        Jika response authenticatednya true berarti
        loginnya sukses
        '''
        if loginResponse['authenticated']:
            print("    {}Berhasil login!".format(self.YELLOW))
            self.status_login = True
            self.user_id = loginResponse['userId']
        else:
            print("    {}Gagal login!".format(self.RED))

    '''
    Mendapatkan random hastag dari
    data config
    '''
    def getRandomHastag(self):
        with open('data_config.yml', 'r') as f:
            yaml.warnings({'YAMLLoadWarning': False})
            config = yaml.load(f)

            index = random.randint(0, len(config['tag'])-1)
            return config['tag'][index]

    '''
    Mendapatkan random komentar dari
    data config
    '''
    def getRandomComment(self):
        with open('data_config.yml', 'r') as f:
            yaml.warnings({'YAMLLoadWarning': False})
            config = yaml.load(f)

            index = random.randint(0, len(config['comments'])-1)
            return config['comments'][index]

    '''
    Mendapatkan random user agents
    dari agents file
    '''
    def getUsersAgents(self):
        with open('agents', 'r') as f:
            agents = f.readlines()
            index = random.randint(0, len(agents)-1)

            return agents[index].replace('\n', '')

