audioTitle = document.getElementById('song-title')
audioDescription = document.getElementById('song-description')
audioCover = document.getElementById('song-cover')
buttonUpdate = document.getElementById('button-update')
buttonNext = document.getElementById('button-next')
buttonStatus = document.getElementById('button-status')

base_url = 'http://localhost:8080/internal/main/'

// setInterval(function () {
//     let url = base_url + 'track'
//     fetch(url).then(function (response) {
//         console.log(response.json())
//         return response.json();
//     }).then(function (data) {
//         console.log(data);
//     }).catch(function (err) {
//         console.log('Fetch Error :-S', err);
//     });
// }, 1000);

buttonStatus.onclick = function () {
    url = base_url + 'track'
    fetch(url, {
        method: 'GET',
    })
        .then((response) => response.json())
        .then(function (data) {
            console.log(data)
            const {
                artist_name, track_numer, track_name, cover
            } = data
            audioTitle.innerText = `${artist_name} - ${track_numer}. ${track_name}`
            audioCover.setAttribute('src', "data:image/jpg;base64," + cover);
        })
}

buttonUpdate.onclick = function () {
    let url = base_url + 'update'
    fetch(url).then(function (response) {
        data = response.json()
        console.log(data)
        return data;
    }).then(function (data) {
        console.log(data);
    }).catch(function (err) {
        console.log('Fetch Error :-S', err);
    });
}

buttonNext.onclick = function () {
    let url = base_url + 'next'
    fetch(url).then(function (response) {
        data = response.json()
        console.log(data)
        return data;
    }).then(function (data) {
        console.log(data);
    }).catch(function (err) {
        console.log('Fetch Error :-S', err);
    });
}