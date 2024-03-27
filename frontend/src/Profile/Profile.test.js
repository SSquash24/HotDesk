import { render, screen } from '@testing-library/react';
import Profile from './Profile';

test('renders without crashing', () => {
  render(<Profile />);
});

test('page has calendar', () => {
  render(<Profile />);
  expect(screen.getByText(new Date().getFullYear())).toBeInTheDocument()
})