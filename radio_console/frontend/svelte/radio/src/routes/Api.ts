import axios from "axios";
import {currentMount} from "../stores";

export enum Mount {
    tech = 'tech',
    ambient = 'ambient',
    sex = 'sex',
    rus = 'rus',
    classic = 'classic',
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
        this.mount = $currentMount
        // Проверяем, является ли строка значением перечисления Mount
        if (Object.values(Mount).includes(mount as Mount)) {
            this.mount = mount as Mount;
        }
    }

    streamPath() {
        return `/stream_${this.mount}`;
    }

    streamPort() {
        return 8000 + this.intMap[this.mount]
    }
}

export class ApiController {
    url: URL
    mount: Mount

    constructor() {
        currentMount.subscribe(value => this.mount = value)
        this.url = new URL(document.URL)
    }

    async trackRequest() {
        let url = new URL(this.url)
        url.port = '8080'
        url.pathname = `${this.mount}/track`
        try {
            return await axios.get(url.toString());
        } catch (exception) {
            console.log(exception)
        }
    }

    async coverRequest() {
        let url = new URL(this.url.toString())
        url.port = '8080'
        url.pathname = `${this.mount}/cover`
        try {
            return await axios.get(url.toString());
        } catch (exception) {
            console.log(exception)
        }
    }
}
