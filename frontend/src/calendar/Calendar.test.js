import { render, screen, waitFor } from '@testing-library/react';
import Calendar from './Calendar';
import { TokenContext } from '../Navigator/Navigator';
import fetchMock from 'jest-fetch-mock';
import '../config'


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
        expect(screen.getByText(global.config.today.getFullYear())).toBeInTheDocument()
    })

    test('tells you month', () => {
        expect(screen.getByText(global.config.today.toLocaleString('default', { month: 'long' }))).toBeInTheDocument();
    })

    test('tells you today', () => {
        expect(screen.getByTestId('table-content').querySelector('.today')).toHaveTextContent(global.config.today.getDate());
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
            { date: new Date(global.config.today.getFullYear(), global.config.today.getMonth(), 14), seat: 'A1' },
            { date: new Date(global.config.today.getFullYear(), global.config.today.getMonth(), 16), seat: 'B2' },
        ];

        fetch.mockResponseOnce(JSON.stringify(mockResponse));

        render(
            <TokenContext.Provider value={{ token: "test", setToken: setToken }}>
                <Calendar />
            </TokenContext.Provider>
        );

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(global.config.api_myBookings, {
                method: "GET",
                headers: {
                    'Authorization': 'test',
                },
            });
        })

        await waitFor(() => {
            mockResponse.forEach(booking => {
                expect(screen.getByText(booking.date.getDate()).closest("span")).toHaveClass("booked")
            });
        })
        
    });
})