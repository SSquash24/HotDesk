import '../config'
import { render, waitFor, screen } from '@testing-library/react';
import Navigator from './Navigator';
import fetchMock from 'jest-fetch-mock';



describe('NavigatorComponent', () => {

    beforeEach(() => {
        fetchMock.enableMocks();
        fetchMock.doMock();
        fetch.resetMocks();
    })

    test('renders without crashing', () => {
        render(<Navigator />)
    })

    test('makes a GET request to /users/me when page loads', async () => {
        render(<Navigator />);

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(global.config.api_path + 'users/me', {
                method: 'GET',
                headers: {
                    "accept": "application/json",
                    "Authorization": null
                },
            });
        });

    });

    test('redirects to /login if GET /users/me request is denied', async () => {
        fetch.mockReject(() => Promise.reject("API is down"));

        render(<Navigator />);

        await waitFor(() => {
            expect(screen.getAllByText("Login")[0]).toBeInTheDocument();
        });
    });

    test('redirects to / if GET /users/me request is accepted', async () => {
        fetch.mockResponse(JSON.stringify({ username: 'testUser' }))
        render(<Navigator />);
    
        await waitFor(() => {
          expect(screen.getAllByText('Profile')[0]).toBeInTheDocument();
        });
    });


})