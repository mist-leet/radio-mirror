export interface Track {
    id: number;
    name: string;
    track_number: number;
    duration: string;
    is_active: boolean;
}

export interface Album {
    name: string;
    year: number;
}

export interface Artist {
    name: string;
}

export interface Rows {
    album: Album;
    artist: Artist;
    track_list: Track[];
}

export interface TrackRow {
    artistName: string;
    albumName: string;
    albumYear: number;
    trackName: string;
    trackDuration: string;
    activeClass: string;
}