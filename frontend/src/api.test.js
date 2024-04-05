
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { createMemoryHistory } from 'history';
import fetchMock from 'jest-fetch-mock';
import Login from './Login/Login';
import { TokenContext } from './Navigator/Navigator';
import './config';
import Navigator from './Navigator/Navigator';
import Calendar from './calendar/Calendar';


beforeEach(() => {
  fetchMock.enableMocks();
  fetchMock.doMock();
});

describe('LoginPage', () => {
    let setToken;

    beforeEach(() => {
      setToken = jest.fn();
      fetch.mockResponseOnce(JSON.stringify({ access_token: 'testToken' })); // Mocked response
      render(
          <TokenContext.Provider value={{ token: "test", setToken: setToken }}>
              <Login />
          </TokenContext.Provider>
      );
      expect(setToken).toHaveBeenCalledTimes(0);
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



describe('Navigator', () => {
    beforeEach(() => {
        fetch.resetMocks();
    });

    test('makes a GET request to /users/me when page loads', async () => {
        fetch.mockResponseOnce(JSON.stringify({ username: 'testUser' }));

        render(<Navigator />);

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(global.config.api_path + 'users/me', {
                method: 'GET',
                headers: {
                    // "Content-type": "application/x-www-form-urlencoded",
                    "accept": "application/json",
                    "Authorization": null
                },
            });
        });
    });


    test('redirects to /login if GET /users/me request is denied', async () => {
        const history = createMemoryHistory()
        fetch.mockReject(() => Promise.reject("API is down"));

        render(
            // <Router history={history}>
                <Navigator history={history} />
            // </Router>
        );

        await waitFor(() => {
            expect(history.location.pathname).toBe('/login');
        });
    });

    test('redirects to / if GET /users/me request is accepted', async () => {
        const history = createMemoryHistory()
        fetch.mockResponseOnce(JSON.stringify({ username: 'testUser' }));
    
        render(
          <Navigator history={history} />
        );
    
        await waitFor(() => {
          expect(history.location.pathname).toBe('/');
        });
      });
    });

    test('sends GET request to bookings/me and shows current bookings when logged in', async () => {
      // const history = createMemoryHistory();
      const setToken = jest.fn();
      const mockResponse = [
        { date: '2022-12-01', seat: 'A1' },
        { date: '2022-12-02', seat: 'B2' },
      ];
      
      fetch.mockResponseOnce(JSON.stringify(mockResponse));
    
      render(
        <TokenContext.Provider value={{token: "test", setToken: setToken}}>
          {/* <Router history={history}> */}
            <Calendar />
          {/* </Router> */}
        </TokenContext.Provider>
      );
    
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/bookings/me', {
          headers: {
            'Authorization': 'test',
          },
        });
        
        mockResponse.forEach(booking => {
          expect(screen.getByText(new Date(booking.date).toDateString())).toBeInTheDocument();
        });
      });
    });
