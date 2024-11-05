
#  Install

1. cLone repository
2. modify ```radio_console/env/.env```
3. install rclone
```sudo apt install rclone```
4. run ```rclone config``` and modify ```disk/rclone_script.sh```->```token```


# links
 - ezstream help: https://manpages.debian.org/testing/ezstream/ezstream.1.en.html


# local urls
 - http://localhost:8001/admin/
 - http://localhost:8001/stream_main
 - http://localhost:8002/admin/

### utils

convert flac -> mp3
```bash
for file in *.flac; do ffmpeg -i "$file" -q:a 0 -map_metadata 0 "${file%.flac}.mp3"; done
```