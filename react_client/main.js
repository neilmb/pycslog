import {Pycslog} from './pycslog.jsx'
import React from 'react'
import ReactDOM from 'react-dom'

const title = 'My Minimal React Webpack Babel Setup';

console.log("loaded main.js???");

ReactDOM.render(
  <div>{title}</div>,
  document.getElementById('root')
);

module.exports = {
  Pycslog: Pycslog,
  ReactDOM: ReactDOM,
  React: React
}
