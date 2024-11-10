<style>
    /* Левое меню */
    .menu-rows {
        display: flex;
        flex-direction: column;
        gap: 20px;
        /*left: 0;*/
        /*top: 20%;*/
        color: #fff;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7); /* Черная полупрозрачная тень */
        font-size: 24px;
    }
</style>

<script>
    import ControlRow from "./ControlRow.svelte";
    let {rows} = $props()
</script>

<div class="menu-rows">
    {#each rows as row}
        <ControlRow text={row}/>
    {/each}
</div>