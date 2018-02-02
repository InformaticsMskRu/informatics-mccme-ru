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
