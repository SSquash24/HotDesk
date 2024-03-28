import Profile from '../Profile/Profile';
import Book from '../Book/Book'
import Logout from '../Logout/Logout'
import Login from '../Login/Login'
import './Navigator.css'


import {
    createContext,
    useState,
} from 'react';

import {
    BrowserRouter as Router,
    Routes,
    Route,
    NavLink,
    Navigate,
  } from "react-router-dom";

export const TokenContext = createContext(null)

function Navigator() {

    const [token, setToken] = useState(null)
    const [uInfo, setUInfo] = useState(null)

    const authorize = async () => {
        try {
            const response = await fetch(global.config.api_path + 'users/me', {
                headers: {
                    'Authorization': token
                }
            })
            if (response.ok) {
                setUInfo(await response.json())
            }
            else {
                setUInfo(null)
            }
        } catch {
            if (uInfo !== null)
                setUInfo(null)
            else {
                alert("Failed to connect to server")
            }
        }
    }

    authorize() //attempt to authorize, if successfull a refresh will occur


    let pages; //pages will exist or not based on whether user is validated
    if (uInfo === null) {
        pages = <>
                <Route path="/login" element={<Login />} />
                <Route path='*' element={<Navigate to="/login" />}/>
            </>
    } else {
        pages = <>
                <Route exact path="/" element={<Profile />} />
                <Route exact path="/book" element={<Book />} />
                <Route exact path="/logout" element={<Logout />} />
                <Route path='*' element={<Navigate to="/" />}/>
            </>
    }

    return (
        <Router>

            {uInfo !== null && <nav className='navbar'>
                <NavLink to='/'>Profile</NavLink>
                <NavLink to='/book'>Book</NavLink>
                <NavLink to='/logout'>Logout</NavLink>
            </nav>}

            <div className='main'>
                <TokenContext.Provider value={{ token: token, setToken: setToken }}>
                    <Routes>
                        {pages}
                    </Routes>
                </TokenContext.Provider>
            </div>
        </Router>
    
    )
}

export default Navigator