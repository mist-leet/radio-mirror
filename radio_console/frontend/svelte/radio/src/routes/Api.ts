import axios from 'axios';
import {currentMount} from "../stores";

export function mountFromText(text: string) {
    let mapping = {
        'tech': Mount.tech,
        'neoclassical': Mount.classic,
        'lounge': Mount.lounge,
        'soundscape': Mount.ambient,
    }
    return mapping[text]
}

export enum Mount {
    tech = 'tech',
    ambient = 'ambient',
    sex = 'sex',
    rus = 'rus',
    classic = 'class',
    lounge = 'lounge',
    other = 'other',
    lofi_house = 'lofi_house',
}

export class MountManager {
    mount: Mount | string;

    intMap = {
        [Mount.tech]: 1,
        [Mount.ambient]: 2,
        [Mount.sex]: 3,
        [Mount.rus]: 4,
        [Mount.classic]: 5,
        [Mount.lounge]: 6,
        [Mount.other]: 7,
        [Mount.lofi_house]: 8,
    };

    constructor() {
        currentMount.subscribe(value => this.mount = value)
    }

    streamURL(): string {
        let url = new URL(document.URL)
        url.port = (8000 + this.intMap[this.mount]) as string
        url.pathname = `/stream_${this.mount}`;
        return url.toString()
    }
}

export class ApiController {
    mount: Mount

    constructor() {
        currentMount.subscribe(value => this.mount = value)
    }

    async trackRequest() {
        let url = new URL(document.URL)
        url.port = '8080'
        url.pathname = `${this.mount}/track`
        try {
            return await axios.get(url.toString());
        } catch (exception) {
            console.log(exception)
        }
    }

    async nextTrackRequest() {
        let url = new URL(document.URL)
        url.port = '8080'
        url.pathname = `${this.mount}/next`
        try {
            return await axios.get(url.toString());
        } catch (exception) {
            console.log(exception)
        }
    }

    async coverRequest() {
        let url = new URL(document.URL)
        url.port = '8080'
        url.pathname = `${this.mount}/cover`
        const config = {url: url.toString(), method: "get", responseType: "blob"} as axios.AxiosRequestConfig
        return await axios.request(config)
    }
}
