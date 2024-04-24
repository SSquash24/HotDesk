import { useState, useContext } from "react";
import { TokenContext } from "../Navigator/Navigator";
import Calendar from "../calendar/Calendar";
import './book.css'



function Book() {

    const [date, setDate] = useState(new Date());
    const [seats, setSeats] = useState('-')
    const [doInit, setInit] = useState(true)
    const { token } = useContext(TokenContext)


    function getVacancies(day) {
        let lcldate = new Date(day.year, day.month, day.number)
        lcldate.setDate(lcldate.getDate()+1)
        if (day.isBooked || lcldate <= new Date()) {
            setSeats('-')
        } else {
            fetch(global.config.api_path + "bookings/vacancies?date="
                    + String(day.year).padStart(4, '0')
                    + '-' + String(day.month+1).padStart(2, '0')
                    + '-' + String(day.number).padStart(2, '0')
                , {
                method: "GET",
                headers: {
                    "accept": "application/json",
                    "Authorization": token
                }
            }).then( async (response) => {
                let json = await response.json()
                if (response.ok) {
                    setSeats(json)
                }
                else {
                    setSeats('ERR')
                }

            }).catch((err) => {
                setSeats('ERR, could not connect')  
            })
        }
    }

    const handleCalendarClick = (day) => {
        if (doInit) setInit(false)
        setDate(new Date(day.year, day.month, day.number))
        getVacancies(day)
    };

    const handleBookClick = () => {
        fetch(global.config.api_path + "bookings/book", {
            method: "POST",
            headers: {
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "date": String(date.getFullYear()).padStart(4, '0')
                        + '-' + String(date.getMonth()+1).padStart(2, '0')
                        + '-' + String(date.getDate()).padStart(2, '0')
            })
        }).then(async (response) => {
            if (response.ok) {
                alert("Successful Booking for " + date.toDateString())
            } else {
                let json = await response.json()
                alert("Error booking: Server returned bad response: " + json.detail[0].msg)
            }
        }).catch((err) => {
            alert("Error booking: Failed to connect to server")
        })
    }


    return (
        <div className="Book">
            <h1>Booking Page:</h1>
            <div className="mainContents">
                <div className='bookCalendar'><Calendar onClick={handleCalendarClick} alertToday={doInit} /></div>
                <div className="bookingForm">
                    <h2>Date: {date.toDateString()}</h2>
                    <h3>Seats available: {seats}</h3>
                    <button id="bookButton" data-testid="book-button" onClick={handleBookClick} disabled={typeof(seats) != 'number' || seats <= 0}>Book</button>
                </div>
            </div>
        </div>
    );
}


export default Book