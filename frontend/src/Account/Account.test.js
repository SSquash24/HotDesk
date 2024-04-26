import { render, waitFor, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event'
import Account from './Account';
import { TokenContext } from '../Navigator/Navigator';
import fetchMock from 'jest-fetch-mock';
import '../config';

describe('LogoutPage', () => {

    const setToken = jest.fn()

    beforeEach(() => {
        fetchMock.enableMocks();
        fetchMock.doMock();
        fetch.resetMocks()

        jest.clearAllMocks();
        render(
            <TokenContext.Provider value={{ token: "test", setToken: setToken }}>
                <Account />
            </TokenContext.Provider>
        )
        expect(setToken).toHaveBeenCalledTimes(0)
    })

    test('renders without crashing', () => {
    })

    test('has expected components', () => {
        expect(screen.getByText("Change Password:")).toBeInTheDocument();
        expect(screen.getByText("Logout")).toBeInTheDocument();
    })

    test('logout button resets token', async () => {
        const logoutButton = screen.getByText("Logout");
        userEvent.click(logoutButton);
        await waitFor(() => {
            expect(setToken).toHaveBeenCalledTimes(1);
        })
    })

    test('change password sends api call', async () => {
        const passwordInput = document.getElementById('pwInput')
        const button = screen.getByText("Change")

        userEvent.type(passwordInput, 'testPassword')
        userEvent.click(button)

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                global.config.api_changePassword + "?password=testPassword", {
                method: "POST",
                headers: {
                    "Authorization": "test",
                    "accept": "application/json"
                }
            }
            )
        })
    })

})
