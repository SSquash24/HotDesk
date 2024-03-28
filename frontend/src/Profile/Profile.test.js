import { render, screen } from '@testing-library/react';
import Profile from './Profile';
import { TokenContext } from '../Navigator/Navigator';

import '../config'

const uInfo = {
  username: "John Doe",
  department: "HR"
}

describe('ProfilePage', () => {

  beforeEach(() => {
    const setToken = jest.fn();
    render(
    <TokenContext.Provider value={{token: "test", setToken: setToken}}>
      <Profile uInfo={uInfo} />;
    </TokenContext.Provider>)
    expect(setToken).toHaveBeenCalledTimes(0)
  });


  test('renders without crashing', () => {
  });

  test('page has calendar', () => {
    expect(screen.getByText(new Date().getFullYear())).toBeInTheDocument()
  })

})