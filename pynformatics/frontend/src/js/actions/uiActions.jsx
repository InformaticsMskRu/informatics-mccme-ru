export function toggleSidebar() {
  return {
    type: 'TOGGLE_SIDEBAR',
  }
}


export function windowResize(width, height) {
  return {
    type: 'WINDOW_RESIZE',
    payload: { width, height }
  }
}
