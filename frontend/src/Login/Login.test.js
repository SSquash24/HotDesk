import { render } from '@testing-library/react';
import Login from './Login';
import { TokenContext } from '../Navigator/Navigator';
import  '../config';

describe('LogoutPage', () => {

  beforeEach(() => {
    const setToken = jest.fn()
    render(
      <TokenContext.Provider value={{token: "test", setToken: setToken}}>
        <Login />
      </TokenContext.Provider>
    )
    expect(setToken).toHaveBeenCalledTimes(0)
  })

  test('renders without crashing', () => {
  });

})