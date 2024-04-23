import { useContext } from 'react';
import { TokenContext } from '../Navigator/Navigator';
import './account.css'

function ChangePassword() {

    function handleClick() {
        let newPW = document.getElementById('pwInput').value
        if (window.confirm("Are you sure you want to change your password to '" + newPW + "' ?")) {
          alert('YES')
        }
    }


    return (
      <div className='changePw'>
        <h3>Change Password:</h3>
        <input id='pwInput' type='text' />
        <button onClick={handleClick}>Change</button>
      </div>
    )
}

function Logout() {

    const { setToken } = useContext(TokenContext);

    function handleClick() {
        setToken(null)
    }


    return (
      <div className='Account'>
        <ChangePassword />
        <button className='logoutButton' onClick={handleClick}>Logout</button>
      </div>
    );
  }
  
  export default Logout;