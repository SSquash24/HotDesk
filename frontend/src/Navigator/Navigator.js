import Profile from '../Profile/Profile';
import Book from '../Book/Book'
import Logout from '../Logout/Logout'
import Login from '../Login/Login'
import './Navigator.css'


import {
    createContext,
    useState,
    useEffect
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

    const [state, changeState] = useState({
        uInfo: null,
        token: null,
        validated: false,
        attemptValidation: true
    })


    const setToken = (token) => {
        changeState({
            uInfo: null,
            token: token,
            validated: false,
            attemptValidation: true
        })
    }


    const authorize = async () => {
        try {
            const response = await fetch(global.config.api_path + 'users/me', {
                headers: {
                    'Authorization': state.token
                }
            })
            if (response.ok) {
                changeState({
                    uInfo: await response.json(),
                    validated: true,
                    token: state.token,
                    attemptValidation: false,
                })
            }
            else {
                changeState({
                    uInfo: null,
                    validated: false,
                    token: state.token,
                    attemptValidation: false
                })
            }
        } catch {
            alert("Failed to connect to server")
            if (state.validated)
                changeState({
                    uInfo: null,
                    token: state.token,
                    validated: false,
                    attemptValidation: false
                })
        }
    }


    useEffect(() => {
        if (state.attemptValidation) authorize() //attempt to authorize, if successfull a refresh will occur
    })

    

    let pages; //pages will exist or not based on whether user is validated
    if (!state.validated) {
        pages = <>
                <Route path="/login" element={<Login />} />
                <Route path='*' element={<Navigate to="/login" />}/>
            </>
    } else {
        pages = <>
                <Route exact path="/" element={<Profile uInfo={state.uInfo}/>} />
                <Route exact path="/book" element={<Book />} />
                <Route exact path="/logout" element={<Logout />} />
                <Route path='*' element={<Navigate to="/" />}/>
            </>
    }

    return (
        <Router>

            {state.validated && <nav className='navbar'>
                <NavLink to='/'>Profile</NavLink>
                <NavLink to='/book'>Book</NavLink>
                <NavLink to='/logout'>Logout</NavLink>
            </nav>}

            <div className='main'>
                <TokenContext.Provider value={{ token: state.token, setToken: setToken }}>
                    <Routes>
                        {pages}
                    </Routes>
                </TokenContext.Provider>
            </div>
        </Router>
    
    )
}

export default Navigator