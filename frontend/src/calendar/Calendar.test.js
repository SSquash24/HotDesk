import { render, screen } from '@testing-library/react';
import Calendar from './Calendar';

test('renders without crashing', () => {
  render(<Calendar />);
});

test('tells you year', () => {
  render(<Calendar />)
  expect(screen.getByText(new Date().getFullYear())).toBeInTheDocument()
})

test('tells you month', () => {
  render(<Calendar />);
  expect(screen.getByText(new Date().toLocaleString('default', { month: 'long' }))).toBeInTheDocument();
})

test('tells you today', () => {
  render(<Calendar />);
  expect(screen.getByTestId('table-content').querySelector('.today')).toHaveTextContent(new Date().getDate());
})