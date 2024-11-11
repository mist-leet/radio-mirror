<style>
    .main {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        width: 90%;
        /*max-width: 1200px;*/
        height: 100%;
        position: relative;
    }

    .empty {
        /*width: 10vw;*/
    }

    /* Стили для аудиоплеера */
    #audio {
        display: none; /* скрываем встроенный аудиоплеер */
    }

    @media (max-width: 768px) {
        .main {
            flex-direction: column;
            width: 100%;
        }

        .empty {
            width: 0;
        }
    }
</style>

<script lang="ts">
    import MainCover from "./MainCover/MainCover.svelte";
    import Playlist from "./Playlist/Playlist.svelte";
    import Menu from "./Menu/Menu.svelte";
    import {ApiController, Mount, MountManager} from './Api.ts'
    import {onMount, onDestroy} from 'svelte';
    import type {Rows} from "./Playlist/Track";
    import {currentMount} from "../stores";

    let playlistResponse: Rows = $state()
    let currentCoverPath: string = $state('/img.png')
    let streamURL = $state('');
    let previousAlbum = ''
    let currentAlbum = $derived(playlistResponse?.album?.name)
    let mountManager = new MountManager()

    function updateEverySecond() {
        const apiController = new ApiController()
        apiController.trackRequest().then(value => {
            playlistResponse = value.data as Rows
            // console.log($state.snapshot(playlistResponse));
        });
        if (previousAlbum !== currentAlbum) {
            apiController.coverRequest().then(value => {
                const blob = new Blob([value.data], {type: 'image/jpeg'}); // Замените тип на нужный, если изображение не PNG
                const url = URL.createObjectURL(blob);
                currentCoverPath = url
                console.log(url)
            });
        }
        previousAlbum = currentAlbum
    }

    let interval;
    onMount(() => {
        updateEverySecond(); // Получаем данные один раз при монтировании
        interval = setInterval(updateEverySecond, 1000);
        const unsubscribe = currentMount.subscribe(() => {
            streamURL = mountManager.streamURL();
        });

        return () => clearInterval(interval); // Очищаем таймер при размонтировании компонента
    });
</script>

<div class="main">
    <video controls name="media" id="audio">
        <source id="audio-source" src="{streamURL}" type="audio/mpeg">
    </video>
    <Menu/>
    <MainCover cover="{currentCoverPath}"/>
    <div class="empty"></div>
    <Playlist rows={playlistResponse} cover={currentCoverPath}/>
</div>