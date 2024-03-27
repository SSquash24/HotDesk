import { render } from '@testing-library/react';
import Login from './Login';

test('renders without crashing', () => {
  render(<Login />);
});