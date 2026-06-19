function PlayerCard(props) {
    return (
        <>
    <div className = 'team-section'>
        <h1 className = 'team-title'>{props.honor} Team All-NBA </h1>
        <div className = 'display-card'>
            {props.data?.predictions?.slice(props.start, props.end).map(player => (
            <div key = {player?.[1]} className = 'card-profile'>
                <img className = 'headshot' 
                src = {`https://cdn.nba.com/headshots/nba/latest/260x190/${player?.[1]}.png`}/>
                <div className = 'player-name'>{player?.[0]}</div>
                <div className = 'player-team'> {player?.[2]}</div>
                <div className = 'player-stats'>{player?.[3][0]} / {player?.[3][1]} / {player?.[3][2]}</div>
            </div>))}
        </div>
    </div>
    </>)
}

export default PlayerCard