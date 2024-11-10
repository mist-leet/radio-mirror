<style>
    /* Плейлист */
    .playlist-block {
        /*overflow: hidden;*/
        scrollbar-width: none;
        width: 27vw;
        background-color: #111;
        padding: 15px;
        border-radius: 8px;
        max-height: 80vh;
        /*margin-left: 20px;*/
        margin-left: 10vw;
        overflow-y: scroll; /* Прокрутка по вертикали */
        scrollbar-width: none; /* Для Firefox */
    }

    .playlist-block::-webkit-scrollbar {
        display: none;
    }

    @media (max-width: 768px) {
        .playlist-block {
            width: 100vw;
            margin-left: 0;
        }
    }
</style>
<script lang="ts">
    import PlaylistRow from "./PlaylistRow.svelte";
    import type {Rows, TrackRow} from "./Track";

    function extractRow(data: Rows): TrackRow[] {
        if (!data.track_list) {return []}
        const albumName = data.album.name;
        const albumYear = data.album.year;
        const artistName = data.artist.name;
        const activeTrackIndex = data.track_list.findIndex((item) => (item.is_active))
        return data.track_list.map((item, index) => ({
            artistName: artistName,
            albumName: albumName,
            albumYear: albumYear,
            trackName: item.name,
            trackDuration: item.duration,
            activeClass: index === activeTrackIndex ? 'is-active' : index === activeTrackIndex - 1 ? 'before-active' : '',
        }));
    }

    const defaultRows: Rows = {
        album: {
            name: "1996 - Panorama 94-96",
            year: 1994
        },
        artist: {
            name: "Ab Ovo"
        },
        track_list: [
            {id: 47, name: "Spuma", track_number: 0, duration: "04:02", is_active: false},
            {id: 48, name: "Eldolon", track_number: 1, duration: "02:48", is_active: false},
            {id: 49, name: "The Sky Horses", track_number: 2, duration: "06:26", is_active: true},
            {id: 50, name: "Mnemosyne", track_number: 3, duration: "07:45", is_active: false},
            {id: 51, name: "L'Architecture Secrete", track_number: 4, duration: "04:60", is_active: false},
            {id: 52, name: "Arimathie's Rain", track_number: 5, duration: "06:50", is_active: false},
            {id: 53, name: "Carmina", track_number: 6, duration: "04:58", is_active: false},
            {id: 54, name: "L'Appel Du Froid", track_number: 8, duration: "06:55", is_active: false},
            {id: 55, name: "Aither", track_number: 9, duration: "06:00", is_active: false},
            {id: 56, name: "Panorama", track_number: 11, duration: "06:40", is_active: false}
        ]
    };

    // let rows = $props()
    let {rows = defaultRows} = $props();

    console.log($state.snapshot(rows));
    const trackList = extractRow(rows);
</script>
<div class="playlist-block">
    {#each trackList as row}
        <PlaylistRow {row}/>
    {/each}
</div>
