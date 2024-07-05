import './Player.css'
import Cover from "./Cover/Cover";
import PlayPause from "./PlayerPanel/PlayPause";

export default function Player() {

    return (
        <div className="player-box">
            <Cover/>
            <PlayPause/>
        </div>

    )
}