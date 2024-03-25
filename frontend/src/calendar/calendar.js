import React, { Component } from 'react';
import CalendarDays from './calendar-days';
import './calendar.css'

export default class Calendar extends Component {
    constructor(props) {
        super()

        this.weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        this.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

        this.state = {
            currentDay: new Date(),
            selectedDay: new Date()
        }
        this.handleClick = props.onClick
    }

    changeCurrentDay = (day) => {
        this.setState({ currentDay: new Date(day.year, day.month, 1), selectedDay: new Date(day.year, day.month, day.number) });
        this.handleClick(new Date(day.year, day.month, day.number));
    }

    lastMonth = ()  => {
        let newDate = null;
        if (this.state.currentDay.getMonth() === 0) {
            newDate = new Date(this.state.currentDay.getFullYear() - 1, 11, 31)
        } else {
            newDate = new Date(this.state.currentDay.getFullYear(), this.state.currentDay.getMonth(), 0)
        }
        this.setState({ currentDay: newDate})
    }

    nextMonth = () => {
        let newDate = null;
        if (this.state.currentDay.getMonth() === 11) {
            newDate = new Date(this.state.currentDay.getFullYear() + 1, 0, 1)
        } else {
            newDate = new Date(this.state.currentDay.getFullYear(), this.state.currentDay.getMonth() + 1, 1)
        }
        this.setState({ currentDay: newDate})
    }

    render() {
        return (
            <div className='calendar'>
                <div className='calendar-header'>
                    <div className='header-arrows'>
                        <button onClick={this.lastMonth}>&lt;</button>
                        <button onClick={this.nextMonth}>&gt;</button>
                    </div>
                    <h3>{this.months[this.state.currentDay.getMonth()]}</h3>
                    <h3>{this.state.currentDay.getFullYear()}</h3>
                </div>
                <div className='calendar-body'>
                    <div className='table-header'>
                        {
                            this.weekdays.map((weekday) => {
                                return <div className='weekday'><p>{weekday}</p></div>
                            })
                        }
                    </div>
                    <CalendarDays selected={this.state.selectedDay} day={this.state.currentDay} changeCurrentDay={this.changeCurrentDay} />
                </div>
            </div>
        )
    }
}