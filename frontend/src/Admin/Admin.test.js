import { render, waitFor, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event'
import Admin from './Admin';
import { TokenContext } from '../Navigator/Navigator';
import '../config';
import fetchMock from 'jest-fetch-mock';

describe("Admin page", () => {

    beforeEach(() => {
        fetchMock.enableMocks();
        fetchMock.doMock();
        const setToken = jest.fn()
        fetch.mockReject(() => Promise.reject("No API"))
        render(
            <TokenContext.Provider value={{ token: "test", setToken: setToken }}>
                <Admin />
            </TokenContext.Provider>
        )
        expect(setToken).toHaveBeenCalledTimes(0)
    });

    test("renders without crashing", () => {
    });

    test("Admin page has expected components", () => {
        expect(screen.getByText("Admin:")).toBeInTheDocument();
        expect(screen.getByText("Add new account:")).toBeInTheDocument();
        expect(screen.getByText("Create")).toBeDisabled();
    });

    test("Adding new account sends API call", async () => {
        const usernameInput = document.getElementById("unameInput");
        const passwordInput = document.getElementById("pwInput");
        const departmentInput = document.getElementById("dptInput");
        const button = screen.getByTestId("create-button");

        userEvent.type(usernameInput, "testUser")
        userEvent.type(passwordInput, "testPassword")
        userEvent.type(departmentInput, "testDepartment")


        expect(button).toBeEnabled();
        userEvent.click(button)

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                global.config.api_createUser, {
                method: "POST",
                headers: {
                    "Authorization": "test",
                    "content-type": "application/json",
                    "accept": "application/json"
                },
                body: JSON.stringify({
                    "username": "testUser",
                    "password": "testPassword",
                    "department": "testDepartment",
                    "role": "basic"
                })
            }
            )
        })


    })


})