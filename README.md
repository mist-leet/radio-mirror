
#  Install

### 1. Clone repo
```git clone https://gitlab.com/artemov.ilya.r/radio.git```

### 2. Install dependencies

1. [nvm](https://github.com/nvm-sh/nvm) - nodejs version manager
    
    ```curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash```

2. [rclone](https://rclone.org/) - for local authenticate in Yandex.Disk

    ```sudo -v ; curl https://rclone.org/install.sh | sudo bash```

3. make 

    ```sudo apt-get -y install make```

### 3. Modify config

#### Yandex disk auth
1. Open https://disk.yandex.ru/client/disk, make sure, you are authenticate now
2. Run ```rclone authorize "yandex"```
3. Login in opened browser
4. Copy json from terminal, looks like: 
```
If your browser doesn't open automatically go to the following link: http://127.0.0.1:53682/auth?state=XXX
Log in and authorize rclone for access
Waiting for code...
Got code
Paste the following into your remote machine --->
{"access_token":"XXX","token_type":"bearer","refresh_token":"XXX","expiry":"2077-11-03T01:38:06.58520054+03:00"}
<---End paste
```
5. Paste into ```radio/disk/rclone_script.sh``` into ```token``` field

#### Modify .env ```radio/radio_console/env/.env```
```
POSTGRES_DB=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_HOST=...
POSTGRES_PORT=...
SOURCE_PATH=/source <--- always '/source' 
YANDEX_DISK_PATH=/root/Yandex.Disk/____your Yandex.Disk path____
```

## 4. Run

```make rebuild_frontend``` - rebuild svelte app

```make build``` - rebuild frontend + run docker

```make build_d``` - rebuild frontend + run docker in deamon mode

```make exec -C=ezstream``` - attach to docker container




### utils

convert flac -> mp3
```bash
for file in *.flac; do ffmpeg -i "$file" -q:a 0 -map_metadata 0 "${file%.flac}.mp3"; done
```