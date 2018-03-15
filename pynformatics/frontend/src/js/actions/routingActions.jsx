export function setRedirectUrl(url) {
  return {
    type: 'SET_REDIRECT_URL',
    payload: {url}
  }
}

export function resetRedirectUrl() {
  return {
    type: 'RESET_REDIRECT_URL',
  }
}