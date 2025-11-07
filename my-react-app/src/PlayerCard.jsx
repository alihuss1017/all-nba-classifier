import { useState, useEffect } from "react"
import "./App.css"
import teamColors from "./teamColors"

export default function PlayerCard() {

  const [playerData, setPlayerData] = useState()
  const [playerTeams, setPlayerTeams] = useState()
  const [playerStats, setPlayerStats] = useState()

  useEffect(function() {
    fetch('http://127.0.0.1:8000/players/')
    .then(res => res.json())
    .then(data => setPlayerData(data))
  }, [])


  useEffect(function() {
    fetch('http://127.0.0.1:8000/stats/')
    .then(res => res.json())
    .then(data => setPlayerStats(data))
  }, [])


  useEffect(function() {
    fetch('http://127.0.0.1:8000/teams/')
    .then(res => res.json())
    .then(data => setPlayerTeams(data))
  }, [])



  const playerNames = playerData?.players.map((player, i) => {

    const cardStyle = {
                    backgroundColor: teamColors?.[playerTeams?.teams?.[i]]?.background
                    }

    return <div className = "playerCard">
      <div style = {cardStyle}>
      <p className = "playerName">{player}</p>
        <table className = "playerStat">
          <thead>
            <tr>
              <th>PTS</th>
              <th>TRB</th>
              <th>AST</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              {playerStats?.data[i].map((stat, j) => <td>{stat}</td>)}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  })
  return <>{playerNames}</>
}