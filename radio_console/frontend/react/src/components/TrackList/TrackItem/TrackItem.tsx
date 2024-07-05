import './TrackItem.css'

interface ITrackItemProps {
    artistName: string
    albumName: string
    albumYear: string
    trackName: string
    trackDuration: string
}

export default function TrackItem(props: ITrackItemProps) {
    const {
        artistName,
        albumName,
        albumYear,
        trackName,
        trackDuration,
    } = props
    return (
        <div className="track-item">
            <div className="blured-square"/>
            <div className="track-item-block">
                <div className="track-item-text-part">
                    <div className="track-item-artist-title">{artistName}</div>
                    <div className="track-item-album-title">{albumName}</div>
                    <div className="track-item-album-year">{albumYear}</div>
                </div>
                <div className="track-item-text-part">
                    <div className="track-item-track-title">{trackName}</div>
                    <div className="track-item-track-duration">{trackDuration}</div>
                </div>
            </div>
        </div>
    )
}