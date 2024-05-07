import CalendarDays from './Calendar-days';
import './Calendar.css'

import { TokenContext } from "../Navigator/Navigator";
import { useState, useContext, useEffect } from 'react';

function Calendar(props) {


    const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

    const { token } = useContext(TokenContext)

    const [currentDay, setCurrentDay] = useState(global.config.today)
    const [selectedDay, setSelectedDay] = useState(global.config.today)
    const [booked, setBooked] = useState({
        value: [],
        fetch: true
    })
    const handleClick = props.onClick

    useEffect(() => {
        if (booked.fetch) {

            fetch(global.config.api_myBookings, {
                method: "GET",
                headers: {
                    'Authorization': token
                }
            }).then((response) => {
                if (response.ok) {
                    return response.json().then((json) => {
                        setBooked({
                            value: json.map((elem) => new Date(elem.date)),
                            fetch: false
                        })
                    })
                }
            }).catch((err) => {
                setBooked({
                    value: [],
                    fetch: false
                })
            })
        }
    })


    const changeCurrentDay = (day) => {
        setCurrentDay(new Date(day.year, day.month, 1))
        setSelectedDay(new Date(day.year, day.month, day.number))
        handleClick(day);
    }

    const lastMonth = () => {
        if (currentDay.getMonth() === 0) {
            setCurrentDay(new Date(currentDay.getFullYear() - 1, 11, 31))
        } else {
            setCurrentDay(new Date(currentDay.getFullYear(), currentDay.getMonth(), 0))
        }
    }

    const nextMonth = () => {
        if (currentDay.getMonth() === 11) {
            setCurrentDay(new Date(currentDay.getFullYear() + 1, 0, 1))
        } else {
            setCurrentDay(new Date(currentDay.getFullYear(), currentDay.getMonth() + 1, 1))
        }
    }

    return (
        <div className='calendar'>
            <div className='calendar-header'>
                <div className='header-arrows'>
                    <button onClick={lastMonth}>&lt;</button>
                    <button onClick={nextMonth}>&gt;</button>
                </div>
                <h3>{months[currentDay.getMonth()]}</h3>
                <h3>{currentDay.getFullYear()}</h3>
            </div>
            <div className='calendar-body'>
                <div className='table-header'>
                    {
                        weekdays.map((weekday) => {
                            return <div key={weekday} className='weekday'><p>{weekday}</p></div>
                        })
                    }
                </div>
                <CalendarDays selected={selectedDay} day={currentDay} changeCurrentDay={changeCurrentDay} booked={booked.value} alertToday={props.alertToday && !(booked.fetch)} />
            </div>
        </div>
    )
}


export default Calendar