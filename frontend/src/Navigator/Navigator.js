import Home from '../Home/Home';
import Book from '../Book/Book'
import Account from '../Account/Account'
import Login from '../Login/Login'
import './navigator.css'


import {
    createContext,
    useEffect,
    useState
} from 'react';

import {
    BrowserRouter as Router,
    Routes,
    Route,
    NavLink,
    Navigate,
} from "react-router-dom";

import usePersistState from '../usePersistState';
import Admin from '../Admin/Admin';

export const TokenContext = createContext(null)

function Navigator(props) {

    const [state, changeState] = usePersistState({
        uInfo: null,
        token: null,
        validated: false,
    }, 'general')

    const [tryValidation, setValidation] = useState(true)

    const setToken = (token) => {
        changeState({
            uInfo: null,
            token: token,
            validated: false,
        })
        setValidation(true)
    }


    const authorize = () => {
        fetch(global.config.api_path + 'users/me', {
            method: "GET",
            headers: {
                'Authorization': state.token,
                "accept": "application/json"
            }
        }).then(async (response) => {
            setValidation(false)
            if (response.ok) {
                let json = await response.json();
                changeState({
                    uInfo: json,
                    validated: true,
                    token: state.token,
                })
            }
            else {
                changeState({
                    uInfo: null,
                    validated: false,
                    token: state.token,
                })
            }
        }).catch((err) => {
            alert("Failed to connect to server")
            setValidation(false)
            if (state.validated) {
                changeState({
                    uInfo: null,
                    token: state.token,
                    validated: false,
                })
            }
        })

    }


    useEffect(() => {
        if (tryValidation) authorize() //attempt to authorize, if successfull a refresh will occur
    })



    let pages; //pages will exist or not based on whether user is validated
    if (!state.validated) {
        pages = <>
            <Route path="/login" element={<Login />} />
            <Route path='*' element={<Navigate to="/login" />} />
        </>
    } else {
        pages = <>
            <Route exact path="/" element={<Home uInfo={state.uInfo} />} />
            <Route exact path="/book" element={<Book />} />
            <Route exact path="/account" element={<Account />} />
            {state.uInfo.role === "admin" && <Route exact path="/admin" element={<Admin />} />}
            <Route path='*' element={<Navigate to="/" />} />
        </>
    }

    return (
        <Router props>

            {state.validated && <nav className='navbar'>
                <NavLink to='/'>Home</NavLink>
                <NavLink to='/book'>Book</NavLink>
                {state.uInfo.role === "admin" && <NavLink to='/admin'>Admin</NavLink>}
                <NavLink to='/account'>Account</NavLink>
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