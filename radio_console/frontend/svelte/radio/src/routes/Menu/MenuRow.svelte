<style>
    .menu-row a {
        color: #fff;
        font-size: 1.5em;
        text-decoration: none;
        transition: color 0.3s;
    }

    .is-selected {
        text-decoration: underline;
    }

    .menu-row a:hover {
        color: #888;
        text-decoration: underline;
        cursor: pointer;
    }
</style>

<script lang="ts">
    import {currentMount} from "../../stores";
    import {mountFromText, Mount} from '../Api.ts'

    function onClick(event) {
        currentMount.set(mountFromText(event.target?.innerText) as Mount);
    }

    let {text} = $props()
    let selectedCalss = $state('');

    currentMount.subscribe(value => {
        if (value === mountFromText(text)) {
            selectedCalss = 'is-selected'
        } else {
            selectedCalss = ''
        }
    })
</script>

<div class="menu-row {selectedCalss}">
    <a on:click="{onClick}">{text}</a>
</div>