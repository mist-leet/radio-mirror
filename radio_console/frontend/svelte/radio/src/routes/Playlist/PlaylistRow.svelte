<style>
    .track-row {
        display: flex;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #333;
    }

    .track-row:last-child {
        border-bottom: none;
    }

    .track-cover-block {
        margin-right: 15px;
    }

    .track-cover {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
    }

    /* Информация о треке */
    .track-info {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        flex-grow: 1;
        color: #fff;
    }

    .artist-info-block {
        display: flex;
        justify-content: space-between;
        text-align: right;
    }

    .artist-title {
        text-align: left;
        font-weight: bold;
        font-size: 1em;
    }

    .album-title {
        text-align: right;
        font-size: 0.9em;
        color: #aaa;
    }

    .track-info-block {
        margin-top: 5px;
    }

    .track-name {
        font-size: 0.9em;
        color: #ccc;
    }

    .additional-info {
        display: flex;
        justify-content: space-between;
        font-size: 0.8em;
        color: #888;
        margin-top: 5px;
    }

    .is-active {
        background-color: #333;
        border-bottom: 0px;
        width: 105%;
        margin-left: -2.5%;
        border-radius: 8px;
        padding: 2.5%;
    }

    .before-active {
        border-bottom: 0px;
    }

</style>
<script lang="ts">
    import type {TrackRow} from "./Track";
    let {
        row,
        cover = '/img.png'
    } = $props()
</script>

<div class="track-row {row.activeClass}">
    <div class="track-cover-block">
        <img class="track-cover" src="{cover}">
    </div>
    <div class="track-info">
        <div class="artist-info-block">
            <div class="artist-title">{row.artistName}</div>
            <div class="album-title">{row.albumName}</div>
        </div>
        <div class="track-info-block">
            <div class="track-name">{row.trackName}</div>
        </div>
        <div class="additional-info">
            <div class="album-year">{row.albumYear}</div>
            <div class="track-duration">{row.trackDuration}</div>
        </div>
    </div>
</div>