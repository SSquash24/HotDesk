import { render, screen } from '@testing-library/react';
import Calendar from './Calendar';
import { TokenContext } from '../Navigator/Navigator';
import '../config'

describe('Calendar', () => {

  beforeEach(() => {
    const setToken = jest.fn();
    render(
    <TokenContext.Provider value={{token: "test", setToken: setToken}}>
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
