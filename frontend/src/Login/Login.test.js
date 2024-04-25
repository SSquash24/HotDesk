import { render, waitFor, screen, fireEvent } from '@testing-library/react';
import Login from './Login';
import { TokenContext } from '../Navigator/Navigator';
import '../config';
import fetchMock from 'jest-fetch-mock';

// describe('LogoutPage', () => {

//     beforeEach(() => {
//         const setToken = jest.fn()
//         render(
//             <TokenContext.Provider value={{ token: "test", setToken: setToken }}>
//                 <Login />
//             </TokenContext.Provider>
//         )
//         expect(setToken).toHaveBeenCalledTimes(0)
//     })

//     test('renders without crashing', () => {
//     });

// })

describe('LoginPage', () => {
    let setToken;

    beforeEach(() => {
        fetchMock.enableMocks();
        fetchMock.doMock();
        setToken = jest.fn();
        fetch.mockResponseOnce(JSON.stringify({ access_token: 'testToken' })); // Mocked response
        render(
            <TokenContext.Provider value={{ token: "test", setToken: setToken }}>
                <Login />
            </TokenContext.Provider>
        );
        expect(setToken).toHaveBeenCalledTimes(0);
    });

    test('renders without crashing', () => {

    });

    test('login button makes a POST request to /login with username and password', async () => {
        const usernameInput = document.getElementById('unameInput');
        const passwordInput = document.getElementById('pwInput');
        const loginButton = screen.getByTestId('login-button');

        fireEvent.change(usernameInput, { target: { value: 'testUser' } });
        fireEvent.change(passwordInput, { target: { value: 'testPassword' } });
        fireEvent.click(loginButton);

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                global.config.api_path + 'login', {
                method: 'POST',
                headers: {
                    "Content-type": "application/x-www-form-urlencoded",
                    "accept": "application/json"
                },
                body: `username=testUser&password=testPassword`
            }
            );
            expect(setToken).toHaveBeenCalledWith('bearer testToken');
        });
    });
});