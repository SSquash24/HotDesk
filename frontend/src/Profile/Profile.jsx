import { useState } from 'react';
import Calendar from '../calendar/Calendar';


function UserInfo(props) {


  return (
    <div className="UInfo">
      <p >
        name: {props.uInfo.username} <br/>
        Team: {props.uInfo.department}
      </p>
      <h3>Today's seat: {props.uInfo.seat}</h3>
    </div>
  );
}

function Bookings() {

  const [date, setDate] = useState(new Date())

  const handleCalendarClick = (day) => {
    setDate(day)
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

function App(props) {
  return (
    <div className="App">
      <h1>Profile</h1>
      <UserInfo uInfo={props.uInfo} />
      <Bookings props />
    </div>
  );
}

export default App;
