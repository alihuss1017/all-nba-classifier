import basketball from './assets/header.png'
export default function Header() {
    return <header>
                <div className = 'header-top'>
                    <img src = {basketball}/>
                    <h1>All-NBA Teams Predictor</h1>
                </div>
            <center><h2> Last updated: June 18, 2026</h2></center>
           </header>
}
