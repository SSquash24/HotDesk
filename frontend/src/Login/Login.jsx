import { TokenContext } from "../Navigator/Navigator";
import { useContext } from "react";
import './login.css'

function Login(props) {

    const { setToken } = useContext(TokenContext);

    const handleButton = function () {
        var details = {
            'username': document.getElementById("unameInput").value,
            'password': document.getElementById("pwInput").value
        }

        var formBody = [];
        for (var property in details) {
            var encodedKey = encodeURIComponent(property);
            var encodedValue = encodeURIComponent(details[property]);
            formBody.push(encodedKey + "=" + encodedValue);
        }
        formBody = formBody.join("&");

        fetch(global.config.api_path + 'login', {
            method: 'POST',
            headers: {
                "Content-type": "application/x-www-form-urlencoded",
                "accept": "application/json"
            },
            body: formBody
        }).then(async (response) => {
            if (response.ok) {
                let json = await response.json();
                setToken("bearer " + json.access_token)
            }
            else {
                alert("Invalid credentials! Please try again")
            }
        })
    }

    return (
        <div className="Login">
            <h1>Login</h1>
            <div className="form">
                <h3>Username:</h3>
                <input id="unameInput"></input>
                <h3>Password:</h3>
                <input id="pwInput"></input>
                <button onClick={handleButton} data-testid="login-button">Login</button>
            </div>
        </div>
    );
}


export default Login