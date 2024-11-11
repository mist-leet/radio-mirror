<style>
    .menu {
        display: flex;
        gap: 100px;
        position: absolute;
        left: 0;
        top: 10%;
        color: #fff;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7); /* Черная полупрозрачная тень */
        font-size: 24px;
    }

    .control-rows {
        display: flex;
        flex-direction: column;
        gap: 20px;
        /*left: 0;*/
        /*top: 20%;*/
        color: #fff;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7); /* Черная полупрозрачная тень */
        font-size: 24px;
    }

    .control-row a {
        color: #fff;
        font-size: 1.5em;
        text-decoration: none;
        transition: color 0.3s;
    }

    .control-row a:hover {
        color: #888;
        text-decoration: underline;
        cursor: pointer;
    }

    @media (max-width: 768px) {
        .menu {
            gap: 10px;
            top: 5%;
            left: 5%
        }
    }
</style>

<script>
    import MenuRows from "./MenuRows.svelte";
    import {currentMount, playerState} from "../../stores";
    import {get} from 'svelte/store'
    import {ApiController} from "../Api.ts";

    let playButtonText = $state('Play')


    function onClickPlayPause(event) {
        playerState.set(!get(playerState));
        playButtonText = !get(playerState) ? 'Play' : 'Pause'
    }

    currentMount.subscribe((value) => {
        playerState.set(false);
        playButtonText = !get(playerState) ? 'Play' : 'Pause'
    })

    function onClickNext(event) {
        const apiController = new ApiController()
        apiController.nextTrackRequest().then(value => {});
    }

</script>

<div class="menu">
    <MenuRows rows={['tech', 'neoclassical', 'lounge', 'soundscape']}/>
    <div class="control-rows">
        <div class="control-row"><a on:click="{onClickPlayPause}">{playButtonText}</a></div>
        <div class="control-row"><a on:click="{onClickNext}">Next</a></div>
    </div>
</div>