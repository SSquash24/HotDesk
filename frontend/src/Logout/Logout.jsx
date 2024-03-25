import './logout.css'

function Logout() {

    function handleClick() {
        alert('Logging out...')

    }

    return (
      <div className='Logout'>
        <button className='logoutButton' onClick={handleClick}>Logout</button>
      </div>
    );
  }
  
  export default Logout;