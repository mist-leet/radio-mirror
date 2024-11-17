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
            max-height: calc(100vh - 100vw);
        }
    }
</style>
<script lang="ts">
    import PlaylistRow from "./PlaylistRow.svelte";
    import type {Rows, TrackRow} from "./Track";

    function extractRow(data: Rows): TrackRow[] {
        if (!data.track_list) {
            return []
        }
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
            name: "Loading",
            year: 2024,
        },
        artist: {
            name: "Loading"
        },
        track_list: [
            {id: 47, name: "Loading...", track_number: 0, duration: "13:37", is_active: false},
            {id: 48, name: "Loading...", track_number: 1, duration: "13:37", is_active: false},
            {id: 49, name:  "Loading...", track_number: 2, duration: "13:37", is_active: true},
            {id: 50, name: "Loading...", track_number: 3, duration: "13:37", is_active: false},
            {id: 51, name:  "Loading...", track_number: 4, duration: "13:37", is_active: false},
            {id: 52, name:  "Loading...", track_number: 5, duration: "13:37", is_active: false},
            {id: 53, name: "Loading...", track_number: 6, duration: "13:37", is_active: false},
            {id: 54, name:  "Loading...", track_number: 8, duration: "13:37", is_active: false},
            {id: 55, name: "Loading...", track_number: 9, duration: "13:37", is_active: false},
            {id: 56, name: "Loading...", track_number: 11, duration: "13:37", is_active: false}
        ]
    };
    let {
        rows = defaultRows,
        cover = '/img.png'
    } = $props()
    // export let rows = defaultRows;
    // export let cover = 'img.png';
</script>
<div class="playlist-block">
    {#each extractRow(rows) as row}
        <PlaylistRow row={row} cover={cover}/>
    {/each}
</div>
