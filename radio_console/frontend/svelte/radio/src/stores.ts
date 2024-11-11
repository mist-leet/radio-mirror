import {writable} from 'svelte/store';
import {Mount} from "./routes/Api";


export const currentMount = writable<Mount>(Mount.lounge);
export const playerState = writable<boolean>(false);

playerState.subscribe((value: boolean) => {
    console.log(value)
})

currentMount.subscribe((value) => {
    console.log(value)
})