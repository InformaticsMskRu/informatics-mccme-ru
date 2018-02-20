import * as _ from 'lodash';


export function getExtensionByFilename(filename) {
  const re = /(?:\.([^.]+))?$/;
  return re.exec(filename)[1];
}


export function getProblemShortNameByNumber(n) {
  const getLetter = (k) => String.fromCharCode(k + 'A'.charCodeAt(0));
  if (n > 26) {
    return getLetter(Math.floor((n - 1) / 26) - 1) + getLetter((n - 1) % 26)
  }
  return getLetter(n - 1);
}


export function getObjectByColor(color) {
  /**
   * "#RRGGBB" => { r, g, b }
   */
  const [r, g, b] = _.map(_.chunk(color.slice(1, 7), 2), pair => parseInt(pair.join(''), 16));
  return { r, g, b }
}


export function getColorByObject(object) {
  const { r, g, b } = object;
  return '#' + _.map([r, g, b], channel => channel.toString(16)).join('');
}


export function getColorBetween(color1, color2, percent) {
  return _.assignWith(color1, color2, (channel1, channel2) => Math.floor((channel1 * (100 - percent) + channel2 * percent) / 100));
}


export function getProblemCellColor(score, theme) {
  const color0 = getObjectByColor(theme.palette['other'][10]);
  const color50 = getObjectByColor(theme.palette['other'][11]);
  const color100 = getObjectByColor(theme.palette['other'][12]);

  let color;
  if (score < 50) {
    color = getColorBetween(color0, color50, score * 2);
  } else {
    color = getColorBetween(color50, color100, (score - 50) * 2);
  }
  return getColorByObject(color);
}
