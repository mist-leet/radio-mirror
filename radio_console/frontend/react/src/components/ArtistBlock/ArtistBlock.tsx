
export interface IArtistBlockProps {
    image: string
    title: string
    description: string
}

export default function ArtistBlock(props: IArtistBlockProps) {
    return (
        <div className="artist-container">
            <img
                className="artist-image"
                src={props.image}
            />
            <div className="artist-title">{props.title}</div>
            <div className="artist-description">{props.description}</div>
        </div>
    )
}