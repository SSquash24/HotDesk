import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event'
import Home from './Home';
import { TokenContext } from '../Navigator/Navigator';

import '../config'

const uInfo = {
    username: "John Doe",
    department: "HR"
}

describe('HomePage', () => {

    beforeEach(() => {
        const setToken = jest.fn();
        render(
            <TokenContext.Provider value={{ token: "test", setToken: setToken }}>
                <Home uInfo={uInfo} />;
            </TokenContext.Provider>)
        expect(setToken).toHaveBeenCalledTimes(0)
    });


    test('renders without crashing', () => {
    });

    test('page has expected components', () => {
        const uinfo = document.getElementsByClassName('UInfo')[0]

        expect(uinfo.innerHTML).toMatch('Name: John Doe');
        expect(screen.getByText("Today's seat:")).toBeInTheDocument();
        expect(uinfo.innerHTML).toMatch('Team: HR');
        expect(screen.getByText(new Date().getFullYear())).toBeInTheDocument();
        expect(screen.getByText('Date: ' + new Date().toDateString())).toBeInTheDocument();
    })


    test('shown date changes when calendar is clicked', async () => {
        let today = new Date();
        let testDate = '15'
        if (testDate === today.getDate()) testDate = '16'
        const toClick = screen.getByText(testDate);
        userEvent.click(toClick)
        today.setDate(testDate)
        await waitFor(() => {
            expect(screen.getByText('Date: ' + today.toDateString())).toBeInTheDocument();
        })
    })

})