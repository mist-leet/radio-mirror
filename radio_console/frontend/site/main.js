function init() {

    function setUpMount() {
        let regexp = RegExp('\/(.+)$')
        mount = regexp.exec(window.location.href)[0]
        player = document.getElementById('audio')
        player.src = `http://0.0.0.0:8001/stream_${mount}`
    }

    function initPLayer() {
        const audio = document.getElementById('audio');
        const playPause = document.getElementById('play-pause');

        playPause.addEventListener('click', () => {
            if (audio.paused) {
                console.log('play')
                audio.play();
                playPause.classList.remove('play');
                playPause.classList.add('pause');
                playPause.textContent = 'Pause';
            } else {
                console.log('pause')
                audio.pause();
                playPause.classList.remove('pause');
                playPause.classList.add('play');
                playPause.textContent = 'Play ';
            }
        });
    }

    function initNextButton() {
        document.getElementById('next-button').addEventListener('click', function () {
            fetch('http://0.0.0.0:8080/tech/next').then((response) => console.log(response))
        })
    }

    function setUpMetadataUpdater() {
        function updateMetaData() {
            fetch('http://0.0.0.0:8080/tech/track')
                .then((res) => {
                    if (!res.ok) {
                        throw new Error
                        (`HTTP error! Status: ${res.status}`);
                    }
                    return res.json();
                })
                .then((data) =>
                    UpdateContent(data)
                )
                .catch((error) =>
                    console.error("Unable to fetch data:", error)
                )
            fetch('http://0.0.0.0:8080/tech/cover')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.blob();
                })
                .then(blob => {
                    const imageUrl = URL.createObjectURL(blob);
                    currentImageURL = imageUrl
                    Array.from(document.getElementsByClassName('cover')).forEach((item) => {
                        item.src = imageUrl;
                        item.width = 500; // Optional: Set width to 500
                        item.height = 500; // Optional: Set height to 500
                    })
                    Array.from(document.getElementsByClassName('track-cover')).forEach(function (item) {
                        item.src = imageUrl;
                        item.width = 500; // Optional: Set width to 500
                        item.height = 500; // Optional: Set height to 500
                    })
                })
                .catch(error => console.error('Error fetching image:', error));
        }

        function UpdateContent(data) {

            let activeTrack = data.track_list.find((track) => track.is_active == true)
            if (activeTrack.name == lastIsActiveTrackName) {
                return
            }
            lastIsActiveTrackName = activeTrack.name

            let playlistBlock = document.getElementsByClassName('playlist-block')[0]
            let currentTrackRows = document.getElementsByClassName('track-row')
            Array.from(currentTrackRows).forEach(function (item) {
                item.remove()
            })

            let artistTitle = data.artist.name
            let albumTitle = data.album.name
            let albumYear = data.album.year

            data.track_list.forEach(function (trackItem) {
                trackTitle = trackItem.name
                trackDuration = trackItem.duration
                let trackRowTemplate = `
            <div class="track-cover-block">
                <img class="track-cover" src="${currentImageURL}">
            </div>
            <div class="track-info">
                <div class="artist-info-block">
                    <div class="artist-title">
                        ${artistTitle}
                    </div>
                    <div class="album-itle">
                        ${albumTitle}
                    </div>
                </div>
                <div class="track-info-block">
                    <div class="track-name">${trackTitle}</div>
                </div>
                <div class="additional-info">
                    <div class="album-year">${albumYear}</div>
                    <div class="track-duration">${trackDuration}</div>
                </div>
            </div>`
                let trackRowBlock = document.createElement('div')
                trackRowBlock.innerHTML = trackRowTemplate
                trackRowBlock.className = 'track-row'
                if (trackItem.is_active == true) {
                    trackRowBlock.className = 'track-row is-active'
                }
                playlistBlock.appendChild(trackRowBlock)
            })
        }

        setInterval(updateMetaData, 5000);
    }

    initPLayer()
    initNextButton()
    setUpMetadataUpdater()
}

let currentImageURL = ''
let lastIsActiveTrackName = ''
let mount = ''
init()
