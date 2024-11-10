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

<script lang="ts">
    import {currentMount} from "../../stores";
    import {Mount} from '../Api.ts'
    function onClick(event) {
        // console.log($currentMount)
        currentMount.set(event.target?.innerText as Mount);

    }
    let {text} = $props()
</script>

<div class="menu-row">

    <a on:click="{onClick}">{text}</a>
</div>