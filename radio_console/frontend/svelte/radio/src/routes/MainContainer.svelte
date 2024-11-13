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

    #audio, #player {
        display: none;
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
    import {ApiController, MountManager} from "./Api.ts"
    import {onMount} from 'svelte';
    import type {Rows} from "./Playlist/Track";
    import {currentMount, playerState} from "../stores";

    let player;
    let playlistResponse: Rows | undefined = $state()
    let currentCoverPath: string = $state('/img.png')
    let streamURL = $state('')

    let previousAlbum = ''
    let currentAlbum = $derived(playlistResponse?.album?.name) as string

    let mountManager = new MountManager()

    function updateEverySecond() {
        const apiController = new ApiController()
        apiController.trackRequest().then(value => {
            playlistResponse = value?.data as Rows
        });
        if (previousAlbum !== currentAlbum) {
            console.log('start load image')
            apiController.coverRequest().then(response => {
                currentCoverPath = URL.createObjectURL(response.data);
                console.log('loaded')
            });
        }
        previousAlbum = currentAlbum
    }

    async function togglePlayer(newState: boolean) {
        if (newState) {
            await player.play();
        } else if (!newState && !player.paused) {
            await player.pause();
        }
    }

    let interval: number;
    onMount(() => {
        updateEverySecond();
        interval = setInterval(updateEverySecond, 5000);
        const unsubscribeOnMountChange = currentMount.subscribe(() => {
            playlistResponse = {} as Rows;
            currentCoverPath = 'img.png'
            updateEverySecond()
            streamURL = mountManager.streamURL();
            console.log('plyaer load')
            player.load()
        });
        const unsubscribeOnPlayerStateChange = playerState.subscribe((value) => {
            togglePlayer(value).then()
        });

        return () => {
            clearInterval(interval);
            unsubscribeOnMountChange();
            unsubscribeOnPlayerStateChange();
        }
    });
</script>

<div class="main">
    <video controls bind:this={player} id="player">
        <source id="audio" src="{streamURL}" type="audio/mpeg">
    </video>
    <Menu/>
    <MainCover cover="{currentCoverPath}"/>
    <Playlist rows={playlistResponse} cover={currentCoverPath}/>
</div>