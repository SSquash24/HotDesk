import { render, screen, waitFor } from '@testing-library/react';
import Book from './Book';
import userEvent from '@testing-library/user-event'
import { TokenContext } from '../Navigator/Navigator';
import '../config';
import fetchMock from 'jest-fetch-mock';

describe('BookPage', () => {

    beforeEach(() => {
        const setToken = jest.fn()

        fetchMock.enableMocks();
        fetchMock.doMock();
        fetch.resetMocks()

        fetch.mockResponse(JSON.stringify(2)) // so there are 2 free seats, the book button is enabled

        render(
            <TokenContext.Provider value={{ token: "test", setToken: setToken }}>
                <Book />
            </TokenContext.Provider>
        )
        expect(setToken).toHaveBeenCalledTimes(0)
    })

    test('renders without crashing', () => {

    });

    test('page has expected components', () => {
        expect(screen.getByText('Booking Page:')).toBeInTheDocument() // title
        expect(screen.getByText(new Date().getFullYear())).toBeInTheDocument() // calendar
        expect(screen.getByText('Book')).toBeInTheDocument() // book button
        expect(screen.getByText('Seats available: -')).toBeInTheDocument()

    })

    test('shown date changes when calendar is clicked', async () => {
        let today = new Date();
        let testDate = '15'
        if (testDate === today.getDate()) testDate = '16'
        const toClick = screen.getByText(testDate);
        userEvent.click(toClick)
        today.setDate(testDate)
        await waitFor(() => {
            expect(screen.getByText('Date: ' + today.toDateString())).toBeInTheDocument();
        })
    })

    test('book button sends valid fetch request', async () => {
        const date = new Date();
        const bookButton = screen.getByTestId('book-button');

        await waitFor(() => {
            expect(bookButton).toBeEnabled()
        })
        userEvent.click(bookButton);


        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                global.config.api_book, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": "test"
                },
                body: JSON.stringify({
                    "date": String(date.getFullYear()).padStart(4, '0')
                        + '-' + String(date.getMonth() + 1).padStart(2, '0')
                        + '-' + String(date.getDate()).padStart(2, '0')
                })
            }
            );
        });
    })


})