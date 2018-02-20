import clone from 'clone';

import isoTheme from './isomorphic/config/themes/themedefault';


const theme = clone(isoTheme);
theme.palette.other = [
  '#A2DA85', // 0, progress bar green
  '#DFDFDF', // 1, line delimiter
  '#90B7FF', // 2, secondary button color
  '#FF6000', // 3, problem status orange
  '#92D673', // 4, problem status green
  '#34BFF6', // 5, problem status blue
  '#407EFF', // 6, menu item selected
  '#343A40', // 7, problem statement text color, primary text color
  '#EE4E49', // 8, tag danger
  '#E6E5E5', // 9, border color
  '#B2BBC3', // 10, problem cell 0 score
  '#F9C999', // 11, problem cell 50 score
  '#92D673', // 12, problem cell 100 score
  '#788195', // 13, problem cell empty
];

export default theme;
