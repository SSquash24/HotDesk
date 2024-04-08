import React from 'react';

import ReactDOM from 'react-dom/client';
import './index.css';
import './config';
import Navigator from './Navigator/Navigator'

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <Navigator />
  </React.StrictMode>
);

