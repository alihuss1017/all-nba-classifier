import { useState, useEffect } from "react"
import "./App.css"
import PlayerCard from "./PlayerCard"

export default function TeamCards() {

  const [playerData, setPlayerData] = useState()
  useEffect(function() {
    fetch('https://nba-backend-latest.onrender.com/predictions')
    .then(res => res.json())
    .then(data => setPlayerData(data))
  }, [])

return (
<div className = 'display-grid'>
  <PlayerCard honor = '1st' data = {playerData} start = {0} end = {5}/>
  <PlayerCard honor = '2nd' data = {playerData} start = {5} end = {10}/>
  <PlayerCard honor = '3rd' data = {playerData} start = {10} end = {15}/>
</div>
)}