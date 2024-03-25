import { useState } from "react";
import Calendar from "../calendar/calendar";
import './book.css'



function Book() {

    const [date, setDate] = useState(new Date());
    const [seats, setSeats] = useState(0)

    const handleCalendarClick = (day) => {
        setDate(day)
        
        let new_seats = 1 //TODO fetch value
        setSeats(new_seats)

    };

    const handleBookClick = () => {
        alert("Booking for " + date.toDateString())
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