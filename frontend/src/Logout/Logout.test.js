import { render } from '@testing-library/react';
import Logout from './Logout';
import { TokenContext } from '../Navigator/Navigator';
import  '../config';

describe('LogoutPage', () => {

  beforeEach(() => {
    const setToken = jest.fn()
    render(
      <TokenContext.Provider value={{token: "test", setToken: setToken}}>
        <Logout />
      </TokenContext.Provider>
    )
    expect(setToken).toHaveBeenCalledTimes(0)
  })

  test('renders without crashing', () => {
  })

})
