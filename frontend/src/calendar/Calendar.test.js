import { render, screen, waitFor } from '@testing-library/react';
import Calendar from './Calendar';
import { TokenContext } from '../Navigator/Navigator';
import fetchMock from 'jest-fetch-mock';
import '../config'


beforeEach(() => {

});

describe('Calendar', () => {

    beforeEach(() => {
        const setToken = jest.fn();
        render(
            <TokenContext.Provider value={{ token: "test", setToken: setToken }}>
                <Calendar />;
            </TokenContext.Provider>)
        expect(setToken).toHaveBeenCalledTimes(0)
    });

    test('renders without crashing', () => {
    });

    test('tells you year', () => {
        expect(screen.getByText(new Date().getFullYear())).toBeInTheDocument()
    })

    test('tells you month', () => {
        expect(screen.getByText(new Date().toLocaleString('default', { month: 'long' }))).toBeInTheDocument();
    })

    test('tells you today', () => {
        expect(screen.getByTestId('table-content').querySelector('.today')).toHaveTextContent(new Date().getDate());
    })

})

describe('Cal API', () => {

    beforeEach(() => {
        fetchMock.enableMocks();
        fetchMock.doMock();
        fetch.resetMocks();
    })

    test('sends GET request to bookings/me and shows current bookings when logged in', async () => {
        const setToken = jest.fn();
        const mockResponse = [
            { date: '2022-12-01', seat: 'A1' },
            { date: '2022-12-02', seat: 'B2' },
        ];

        fetch.mockResponseOnce(JSON.stringify(mockResponse));

        render(
            <TokenContext.Provider value={{ token: "test", setToken: setToken }}>
                <Calendar />
            </TokenContext.Provider>
        );

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/bookings/me', {
                method: "GET",
                headers: {
                    'Authorization': 'test',
                },
            });
        })

        // mockResponse.forEach(booking => {
        //   expect(screen.getByText(new Date(booking.date).toDateString())).toBeInTheDocument();
        // });
    });
})