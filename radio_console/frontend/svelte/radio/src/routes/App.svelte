<script>
    import './Global.css'
    import MainContainer from "./MainContainer.svelte";
</script>

<style>
    /* Стили для аудиоплеера */
    #audio {
        display: none; /* скрываем встроенный аудиоплеер */
    }

</style>

<video controls name="media" id="audio">
    <source id="audio-source" src="http://0.0.0.0:8001/stream" type="audio/mpeg">
</video>

<MainContainer/>