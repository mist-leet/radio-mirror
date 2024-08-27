let button = document.getElementById('play-button')
button.addEventListener('click', function () {
    console.log('event click')
    fetchJSONData()
})
document.getElementById('next-button').addEventListener('click', function () {
    console.log('event click')
    fetch('http://0.0.0.0:8888/tech/next').then((response) => console.log(response))
})


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

}

var myInterval = setInterval(updateMetaData, 1000);

function fetchJSONData() {
    console.log('fetch')
    fetch('example.json')
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
}


function UpdateContent(data) {
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
                <img class="track-cover" src="img.png">
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