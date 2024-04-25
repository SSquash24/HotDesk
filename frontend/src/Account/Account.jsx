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
        <div>
            <div className='changePw sideBySide'>
                <div className='sideBySide'>
                    <p className='padded'>Change Password:</p>
                    <input id='pwInput' type='text' />
                </div>
                <div className='centered'>
                    <button id="changeButton" onClick={handleClick}>Change</button>
                </div>
            </div>
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
            <h1>Account:</h1>
            <div>
                <ChangePassword />
                <div className='centered'>
                    <button id='logoutButton' onClick={handleClick}>Logout</button>
                </div>
            </div>
        </div>
    );
}

export default Logout;