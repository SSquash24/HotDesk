import { useContext } from 'react';
import { TokenContext } from '../Navigator/Navigator';
import './account.css'



function ChangePassword() {

    const { token } = useContext(TokenContext)

    function handleClick() {
        let newPW = document.getElementById('pwInput').value
        if (window.confirm("Are you sure you want to change your password to '" + newPW + "' ?")) {
            fetch(global.config.api_changePassword +  "?password=" + newPW, {
                method: "POST",
                headers: {
                    "Authorization": token,
                    "accept": "application/json"
                }
            }).then(async (response) => {
                if (response.ok) {
                    alert("Password Successfully changed!")
                } else {
                    let json = await response.json();
                    if (json.detail[0].msg === undefined) {
                        alert(`Error: ${json.detail}`)
                    } else {
                        alert(`Error: ${json.detail[0].msg}`)
                    }
                }
            }).catch((err) => {
                alert("Error: Could not connect to server")
            })
        }
    }


    return (
        <div>
            <div className='changePw sideBySide'>
                <div>
                    <h3 className='right'>Change Password:</h3>
                    <input id='pwInput' className='right' type='text' />
                </div>
                <div className='left vertCentered'>
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