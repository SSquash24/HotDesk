import { useContext } from 'react';
import { TokenContext } from '../Navigator/Navigator';
import './logout.css'

function Logout() {

    const { setToken } = useContext(TokenContext);

    function handleClick() {
        setToken(null)
    }

    return (
      <div className='Logout'>
        <button className='logoutButton' onClick={handleClick}>Logout</button>
      </div>
    );
  }
  
  export default Logout;