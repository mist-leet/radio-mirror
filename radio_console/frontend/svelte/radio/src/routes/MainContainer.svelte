<style>
    .main {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        width: 90%;
        height: 100%;
        position: relative;
    }

    @media (max-width: 768px) {
        .main {
            flex-direction: column;
            width: 100%;
        }
    }
</style>

<script lang="ts">
    import MainCover from "./MainCover/MainCover.svelte";
    import Playlist from "./Playlist/Playlist.svelte";
    import Menu from "./Menu/Menu.svelte";
    import {ApiController} from "./Api.ts"
    import {onMount} from 'svelte';
    import type {Rows} from "./Playlist/Track";
    import {currentMount} from "../stores";
    import Player from "./Player/Player.svelte";

    let playlistResponse: Rows | undefined = $state()
    let currentCoverPath: string = $state('/img.png')

    let previousAlbum = ''
    let currentAlbum = $derived(playlistResponse?.album?.name) as string
    let needUpdateCover = $derived(currentAlbum != previousAlbum || !currentAlbum || !previousAlbum) as boolean

    function updateData() {
        const apiController = new ApiController()
        apiController.trackRequest().then(
            value => playlistResponse = value?.data as Rows
        );
        if (!needUpdateCover) {return;}
        apiController.coverRequest().then(response => {
            currentCoverPath = URL.createObjectURL(response.data)
            previousAlbum = currentAlbum;
        })
    }

    function startUpdater(): number {
        previousAlbum = ''
        currentCoverPath = 'img.png'
        updateData()
        return setInterval(updateData, 5000);
    }

    onMount(() => {
        let interval = startUpdater()
        const unsubscribeOnMountChange = currentMount.subscribe(() => {
            clearInterval(interval);
            interval = startUpdater();
        });

        return () => {
            clearInterval(interval);
            unsubscribeOnMountChange();
        }
    });
</script>

<div class="main">
    <Player/>
    <Menu/>
    <MainCover cover={currentCoverPath}/>
    <Playlist rows={playlistResponse} cover={currentCoverPath}/>
</div>