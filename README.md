----
links:
 - ezstream help: https://manpages.debian.org/testing/ezstream/ezstream.1.en.html
 - 

---

local urls:
 - http://localhost:8001/admin/
 - http://localhost:8001/stream_main


 - http://localhost:8002/admin/


convert flac -> mp3
```bash
for file in *.flac; do ffmpeg -i "$file" -q:a 0 -map_metadata 0 "${file%.flac}.mp3"; done

```