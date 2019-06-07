# Tasklikes
Tools ini berfungsi untuk melakukan automatic likes pada postingan instagram berdasarkan hastag tertentu. 
Kemudian ia akan mengumpulkan data usernamenya untuk dijelajahi dan ngelike lagi 12 postingan terbarunya.

# Requirements
- Python3 installed on PC

# Supported OS
- Windows
- Linux

# Installation
```
pip3 install -r requirements.txt
```

# Configuration
- Jika kalian ingin deploy ke heroku, silahkan edit file Procfile dengan
isi sebagai berikut
```python
web: python Tasklikes.py --type cron --username yourusername --password yourpassword
```

# How to use
```
python3 Tasklikes.py --type onetime --username yourusername
or 
python3 Tasklikes.py --type cron --username yourusername --password yourpassword
```

# Type
- onetime : Jika ingin mengeksekusi tools dengan sekali jalan
- cron : Jika ingin menggunakan cron sebanyak 30 menit sekali

# Setting Hastag
- Silahkan buka file data_config.yml dan tambahkan hastag sesuka kalian
- Fungsi komentar menurut saya belum stabil
'''
{
  tag: [
    'popular',
    'trending',
    'instagood',
    'like4like',
    'likeforlike',
    'instadaily',
  ],
  comments: [
    'Great post!',
    'Amazing post, please like me',
    'Great! view my profile also',
    'Like for like :)',
    'Cool images when i see, please like me back',
    'Please follow me back :)'
  ]
}
'''

## Note
Jika kalian deploy ke heroku dan kena checkpoint, silahkan buka instagram di smartphone kalian
lalu klik tombol "Ini adalah saya"

# Screenshot
### Contoh result ketika like postingan hastag
![alt text](https://i.imgur.com/lrR7CzI.png "Contoh result ketika like postingan hastag")

### Contoh result ketika like postingan seseorang
![alt text](https://i.imgur.com/f54msGP.png "Contoh result ketika like postingan seseorang")


