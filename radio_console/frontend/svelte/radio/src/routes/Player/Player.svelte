<style>
    #audio, #player {
        display: none;
    }
</style>

<script>

    import {currentMount, playerState} from "../../stores.ts";
    import {onMount} from "svelte";
    import {MountManager} from "../Api.ts";

    let player;
    let {streamURL = ''} = $props()
    let mountManager = new MountManager()

    function togglePlayer(newState) {
        if (newState) {
            player.play();
        } else if (!newState && !player.paused) {
            player.pause();
        }
    }

    async function loadPlayer() {
        await player.load()
    }

    onMount(() => {
        const unsubscribeOnMountChange = currentMount.subscribe(() => {
            streamURL = mountManager.streamURL();
            loadPlayer()
        });
        const unsubscribeOnPlayerStateChange = playerState.subscribe((value) => togglePlayer(value));

        return () => {
            unsubscribeOnMountChange();
            unsubscribeOnPlayerStateChange();
        }
    });

</script>

<video controls bind:this={player} id="player">
    <source id="audio" src="{streamURL}" type="audio/mpeg">
</video>