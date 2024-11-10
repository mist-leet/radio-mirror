import {writable} from 'svelte/store';
import {Mount} from "./routes/Api";


export const currentMount = writable<Mount>(Mount.lounge); // Значение по умолчанию

currentMount.subscribe((value) => {
    console.log(value)
})