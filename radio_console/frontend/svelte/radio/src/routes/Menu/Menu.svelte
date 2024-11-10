<style>
    /* Левое меню */
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
    import ControlRows from "./ControlRows.svelte";
</script>

<div class="menu">
    <MenuRows rows={['tech', 'neoclassical', 'lounge', 'soundscape']}/>
    <ControlRows rows={['play', 'next',]}/>
</div>