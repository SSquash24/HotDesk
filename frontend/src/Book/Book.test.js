import { render, screen } from '@testing-library/react';
import Book from './Book';

test('renders without crashing', () => {
  render(<Book />);
});

test('page has calendar', () => {
  render(<Book />);
  expect(screen.getByText(new Date().getFullYear())).toBeInTheDocument()
})