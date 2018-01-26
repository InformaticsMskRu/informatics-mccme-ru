export function getExtensionByFilename(filename) {
  const re = /(?:\.([^.]+))?$/;
  return re.exec(filename)[1];
}