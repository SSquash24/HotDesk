import { useContext } from "react"
import { TokenContext } from "../Navigator/Navigator"
import "./admin.css"

function NewAcc () {

    const { token } = useContext(TokenContext)

    function handleClick () {
        let uname = document.getElementById("unameInput").value
        let pw = document.getElementById("pwInput").value
        let dpt = document.getElementById("dptInput").value
        let role = document.getElementById("roleInput").value
        
        fetch(global.config.api_path + "users/", {
            method: "POST",
            headers: {
                "accept": "application/json",
                "Authorization": token,
                "content-type": "application/json"
            },
            body: JSON.stringify({
                "username": uname,
                "password": pw,
                "department": dpt,
                "role": role
            })
        }).then(async (response) => {
            let json = await response.json()
            if (response.ok) {
                alert(`Successful account creation for ${json.username}!\n\npassword: ${json.password}\ndepartment: ${json.department}\nrole: ${json.role}`)
            }
            else {
                if (json.detail[0].msg === undefined) {
                    alert(`Error: ${json.detail}`)
                } else {
                    alert(`Error: ${json.detail[0].msg}`)
                }
            }
        }).catch( (err) => {
            alert("Error: failed to connect to server")
        })

    }

    return (
        <div className="newAcc">
            <h3>Add new account:</h3>
            <div className="newAccBody">
                <div className="form">
                    <div className="sideBySide">
                        <p className="padded">Username:</p>
                        <input type="text" id="unameInput"></input>
                    </div> <div />
                    <div className="sideBySide">
                        <p className="padded">Password:</p>
                        <input type="text" id="pwInput"></input>
                    </div> <div />
                    <div className="sideBySide">
                        <p className="padded">Role:</p>
                        <select id="roleInput">
                            <option value="basic">Basic</option>
                            <option value="admin">Admin</option>
                        </select>
                    </div> <div />
                    <div className="sideBySide">
                        <p className="padded">Department:</p>
                        <input type="text" id="dptInput"></input>
                    </div> <div />
                </div>
                <div className="centered">
                    <button id="createButton" onClick={handleClick}>Create</button>
                </div>
            </div>
        </div>
    )
}

function Admin () {

    return (
        <div className="Admin">
            <h1>Admin:</h1>
            <NewAcc />
        </div>
    )
}

export default Admin