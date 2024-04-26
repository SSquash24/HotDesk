// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';
window.alert = () => { };   // hides errors about window.alert not being implemented
window.confirm = () => { return true; }; // any confirmation window automatically returns yes