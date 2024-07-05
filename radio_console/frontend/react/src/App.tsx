import React, {useEffect, useState} from 'react';
import './App.css';
import Player from "./components/Player/Player";
import TrackList, {ITrackData} from "./components/TrackList/TrackList";
import ArtistBlock from "./components/ArtistBlock/ArtistBlock";

export default function Radio() {
    const [data, setData] = useState<ITrackData>()
    // const
    useEffect(() => {
        // fetch('http://localhost:8080')
        fetch('http://localhost:3000/tmp_response_example.json')
            .then((response) => response.json())
            .then((response) => setData(response))
            .catch((err) => {
                console.log(err)
            })
    }, [])
    return (
        <div className="app-container">
            <Player/>
            {data && (
                <><TrackList tracksData={data}/>
                    <ArtistBlock
                        image={data.ArtistInfo.Image}
                        title={data.ArtistInfo.Name}
                        description={data.ArtistInfo.Description}
                    />
                </>
            )}
        </div>

    )
}