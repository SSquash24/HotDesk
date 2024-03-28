function CalendarDays(props) {

    let firstDayOfMonth = new Date(props.day.getFullYear(), props.day.getMonth(), 1);
    let weekdayOfFirstDay = firstDayOfMonth.getDay();
    let currentDays = [];
    let today = new Date();



    let bookedDays = [...props.booked]

    for (let day = 0; day < 42; day++) {
        if (day === 0 && weekdayOfFirstDay === 0) {
            firstDayOfMonth.setDate(firstDayOfMonth.getDate() - 7);
        } else if (day === 0) {
            firstDayOfMonth.setDate(firstDayOfMonth.getDate() + (day - weekdayOfFirstDay));
        } else {
            firstDayOfMonth.setDate(firstDayOfMonth.getDate() + 1)
        }

        let calendarDay = {
            currentMonth: (firstDayOfMonth.getMonth() === props.day.getMonth()),
            date: (new Date(firstDayOfMonth)),
            month: firstDayOfMonth.getMonth(),
            number: firstDayOfMonth.getDate(),
            selected: (firstDayOfMonth.toDateString() === props.selected.toDateString()),
            isToday: (firstDayOfMonth.toDateString() === today.toDateString()),
            isBooked: (bookedDays.length > 0 && firstDayOfMonth.toDateString() === bookedDays[0].toDateString()),
            year: firstDayOfMonth.getFullYear()
        }

        if (bookedDays.length > 0 && firstDayOfMonth.toDateString() === bookedDays[0].toDateString()) {
            bookedDays.shift()
        }

        currentDays.push(calendarDay);
    }


    return (
        <div data-testid='table-content' className="table-content">
            {
                currentDays.map((day) => {
                    return (
                        <div key={day.date.toDateString()} className={'calendar-day' + (day.currentMonth ? " current" : "")
                        + (day.selected ? " selected" : "")}
                        onClick={() => props.changeCurrentDay(day)}>
                            <span className={"calendar-span" + (day.isToday ? " today" : "") + (day.isBooked ? " booked": "")}>
                                <p>{day.number}</p>
                            </span>
                        </div>
                    )
                })
            }
        </div>
    )
}

export default CalendarDays