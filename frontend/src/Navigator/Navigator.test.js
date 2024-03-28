import '../config'
import { render, screen } from '@testing-library/react';
import Navigator from './Navigator';

describe('NavigatorComponent', () => {


    test('renders without crashing', () => {
        render(<Navigator />)
    })
})