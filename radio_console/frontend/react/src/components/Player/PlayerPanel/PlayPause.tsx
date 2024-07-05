import React, {useState} from 'react';
import {ReactComponent as PlayIcon} from '../../../assets/PlayPause_Play.svg';
import {ReactComponent as PauseIcon} from '../../../assets/PlayPause_Pause.svg';
import './PlayPause.css'

function PlayPauseIco() {
    const [isPause, setIcon] = useState<boolean>(false);

    return (
        <div onClick={() => setIcon(!isPause)}>
            {isPause ? <PauseIcon/> : <PlayIcon/>}
        </div>
    );
}

function PlayPause() {
    return (
        <div className="player-panel">
            <div className="before-player-panel">
                <div className="player-panel-ico-left"><PlayIcon/></div>
                <div className="player-panel-line"></div>
            </div>
            <div className="player-button">
                <PlayPauseIco/>
            </div>
            <div className="before-player-panel">
                <div className="player-panel-line"></div>
                <div className="player-panel-ico-right"><PlayIcon/></div>
            </div>
        </div>

    );
}

export default PlayPause;
