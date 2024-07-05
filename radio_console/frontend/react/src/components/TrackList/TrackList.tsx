import TrackItem from "./TrackItem/TrackItem";
import './TrackList.css'

interface ITrackItem {
    Name: string
    Duration: string
    IsActive: boolean | null
}
interface IAlbumData {
    Genre: string
    Name: string
    Year: string
    Image: string
}

interface IArtistData {
    Name: string
    Description: string
    Image: string
}
export interface ITrackData {
    TrackList: ITrackItem[]
    ArtistInfo: IArtistData
    AlbumInfo: IAlbumData
}

interface ITrackListProps {
    tracksData: ITrackData;
}

export default function TrackList(props: ITrackListProps) {

    const trackItems = props.tracksData.TrackList.map((item, index) => (
        <TrackItem
            key={index}
            trackDuration={item.Duration}
            trackName={item.Name}
            albumName={props.tracksData.AlbumInfo.Name}
            albumYear={props.tracksData.AlbumInfo.Year}
            artistName={props.tracksData.ArtistInfo.Name}
        />
    ))
    return (
        <div className="track-list-container">
            {trackItems}
        </div>
    )
}