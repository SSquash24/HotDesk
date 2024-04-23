import { fireEvent, render, waitFor, screen } from '@testing-library/react';
import Account from './Account';
import { TokenContext } from '../Navigator/Navigator';
import  '../config';

describe('LogoutPage', () => {

  const setToken = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks();
    render(
      <TokenContext.Provider value={{token: "test", setToken: setToken}}>
        <Account />
      </TokenContext.Provider>
    )
    expect(setToken).toHaveBeenCalledTimes(0)
  })

  test('renders without crashing', () => {
  })

  test('has logout button', () => {
    expect(screen.getByText("Logout")).toBeInTheDocument();
  })

  test('logout button resets token', async () => {
    const logoutButton = screen.getByText("Logout");
    fireEvent.click(logoutButton);
    await waitFor(() => {
      expect(setToken).toHaveBeenCalledTimes(1);
    })
  })

})
