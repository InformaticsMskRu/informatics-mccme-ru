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
  '#343A40', // 7, problem statement text color
  '#EE4E49', // 8, tag danger
];

export default theme;
