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
pip install -r requirements.txt
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

## Note
Jika kalian deploy ke heroku dan kena checkpoint, silahkan buka instagram di smartphone kalian
lalu klik tombol "Ini adalah saya"

# Screenshot
### Example result when searching diseases
![alt text](https://i.imgur.com/z2zdetC.png "Example result when searching diseases")

### Example result in database
![alt text](https://i.imgur.com/p0jzBJq.png "Example result in database")


