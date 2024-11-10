<style>
    .menu-row a {
        color: #fff;
        font-size: 1.5em;
        text-decoration: none;
        transition: color 0.3s;
    }

    .menu-row a:hover {
        color: #888;
        text-decoration: underline;
        cursor: pointer;
    }
</style>

<script>
    // import currentMount from '../MainContainer.svelte'
    let {text} = $props()
</script>

<div class="menu-row">
    <a>{text}</a>
</div>