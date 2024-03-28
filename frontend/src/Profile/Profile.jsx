import { useState } from 'react';
import Calendar from '../calendar/Calendar';


const user = {
  username: "John Doe",
  team: "XYZ",
  seat: "A1"

}


function UserInfo() {


  return (
    <div className="UInfo">
      <p >
        name: {user.username} <br/>
        Team: {user.team}
      </p>
      <h3>Today's seat: {user.seat}</h3>
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

function App() {
  return (
    <div className="App">
      <h1>Profile</h1>
      <UserInfo/>
      <Bookings/>
    </div>
  );
}

export default App;
