import { useState, useContext } from "react";
import { TokenContext } from "../Navigator/Navigator";
import Calendar from "../calendar/Calendar";
import './book.css'



function Book() {

    const [date, setDate] = useState(new Date());
    const [seats, setSeats] = useState(0)
    const { token } = useContext(TokenContext)


    const handleCalendarClick = (day) => {
        setDate(day)
        
        fetch(global.config.api_path + "bookings/count?date=" + day.toISOString().split('T')[0], {
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
                setSeats(-1)
            }

        })

    };

    const handleBookClick = () => {
        // try {
            fetch(global.config.api_path + "bookings/book", {
                method: "POST",
                headers: {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "date": (date.toISOString().split('T')[0])
                })
            }).then(async (response) => {
                if (response.ok) {
                    alert("Successful Booking for " + date.toDateString())
                } else {
                    let json = await response.json()
                    alert("Error booking: Server returned bad response: " + json.detail[0].msg)
                }
            })
        // } catch {
        //     alert("Error booking: Failed to connect to server")
        // }
    }

    return (
        <div className="Book">
            <h1>Booking Page</h1>
            <div className="mainContents">
                <div className='bookCalendar'><Calendar onClick={handleCalendarClick} /></div>
                <div className="bookingForm">
                    <h2>Date: {date.toDateString()}</h2>
                    <h3>Seats available: {seats}</h3>
                    <button id="bookButton" onClick={handleBookClick} disabled={seats === 0}>Book</button>
                </div>
            </div>
        </div>
    );
}


export default Book