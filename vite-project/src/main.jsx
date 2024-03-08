import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Upload from './Upload.jsx';

// ReactDOM.createRoot(document.getElementById('root')).render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>,
// )

ReactDOM.render(
  <Router>
    <Routes>
      <Route exact path="/" component={App} />
      <Route path="/upload" component={Upload} />

    </Routes>
  </Router>,
  document.getElementById('root')
);
