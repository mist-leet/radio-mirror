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
    import {ApiController, Mount} from './Api.ts'
    import {onMount} from 'svelte';
    import type {Rows} from "./Playlist/Track";

    let playlistResponse: Rows

    // async function updateEverySecond() {
    //     console.log('update')
    //     const apiController = new ApiController()
    //
    //     const value = await apiController.trackRequest();
    //     playlistResponse = value as Rows;
    // }

    function updateEverySecond() {
        console.log('update')
        const apiController = new ApiController()
        apiController.trackRequest().then(value => {
            playlistResponse = value.data as Rows
            console.log(playlistResponse)
        });
        // playlistResponse = value as Rows;
    }

    let interval;
    onMount(() => {
        updateEverySecond(); // Получаем данные один раз при монтировании
        interval = setInterval(updateEverySecond, 1000);
        return () => clearInterval(interval); // Очищаем таймер при размонтировании компонента
    });
</script>

<div class="main">
    <Menu/>
    <MainCover/>
    <div class="empty"></div>
    <Playlist {playlistResponse}/>
</div>