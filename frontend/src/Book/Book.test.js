import { render, screen } from '@testing-library/react';
import Book from './Book';
import { TokenContext } from '../Navigator/Navigator';
import fetchMock from 'jest-fetch-mock'
import  '../config';



describe('BookPage', () => {

  beforeEach(() => {
    const setToken = jest.fn()
    render(
      <TokenContext.Provider value={{token: "test", setToken: setToken}}>
        <Book />
      </TokenContext.Provider>
    )
    expect(setToken).toHaveBeenCalledTimes(0)
  })

  test('renders without crashing', () => {

  });

  test('page has expected components', () => {
    expect(screen.getByText('Booking Page')).toBeInTheDocument() // title
    expect(screen.getByText(new Date().getFullYear())).toBeInTheDocument() // calendar
    expect(screen.getByText('Book')).toBeInTheDocument() // book button
    expect(screen.getByText('Seats available: -')).toBeInTheDocument()

  })

})