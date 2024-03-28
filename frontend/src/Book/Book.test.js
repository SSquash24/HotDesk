import { render, screen } from '@testing-library/react';
import Book from './Book';
import { TokenContext } from '../Navigator/Navigator';
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

  test('page has calendar', () => {
    expect(screen.getByText(new Date().getFullYear())).toBeInTheDocument()
  })

})