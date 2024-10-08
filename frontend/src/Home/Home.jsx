import { useState, useContext } from 'react';
import { TokenContext } from '../Navigator/Navigator';
import Calendar from '../calendar/Calendar';
import './home.css'

function UserInfo(props) {

    const { token } = useContext(TokenContext)
    const [seat, setSeat] = useState({ value: "loading...", toGet: true })

    if (seat.toGet) {
        fetch(global.config.api_seat + "?d="
            + String(global.config.today.getFullYear()).padStart(4, '0')
            + '-' + String(global.config.today.getMonth() + 1).padStart(2, '0')
            + '-' + String(global.config.today.getDate()).padStart(2, '0')
        , {
            method: "GET",
            headers: {
                "Authorization": token
            }
        }).then(async (response) => {
            let json = await response.json()
            if (response.ok) {
                setSeat({
                    value: json.name,
                    toGet: false
                })
            } else {
                if (response.status === 404) {
                    setSeat({
                        value: json.detail,
                        toGet: false
                    })
                } else {
                    setSeat({
                        value: "Err: " + json.detail,
                        toGet: false
                    })
                }
            }
        })
    }

    return (
        <div className="UInfo">
            <p >
                Name: {props.uInfo.username} <br />
                Team: {props.uInfo.department}
            </p>
            <div className="sideBySide">
                <h3>Today's seat:   </h3> <p>{seat.value}</p>
            </div>
        </div>
    );
}

function Bookings() {

    const [date, setDate] = useState(global.config.today)

    const handleCalendarClick = (day) => {
        setDate(new Date(day.year, day.month, day.number))
    }

    return (
        <div className='bookings'>
            <h2>Your Bookings</h2>
            <div className='bookingsContent'>
                <div className='profileCalendar bookingsChild'> <Calendar onClick={handleCalendarClick} /> </div>
                <h3 className='bookingsChild'>Date: {date.toDateString()}</h3>
            </div>
        </div>
    )
}

function Home(props) {
    return (
        <div className="App">
            <h1>Home Page: </h1>
            <UserInfo uInfo={props.uInfo} />
            <Bookings props />
        </div>
    );
}

export default Home;
