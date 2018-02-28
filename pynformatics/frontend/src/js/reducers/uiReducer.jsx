const initialState = {
  sidebarCollapsed: true,
  width: window.innerWidth,
  height: window.innerHeight,
};

export default function reducer(state = initialState, action) {
  switch (action.type) {
    case 'TOGGLE_SIDEBAR':
      return {
        ...state,
        sidebarCollapsed: !state.sidebarCollapsed,
      };

    case 'WINDOW_RESIZE':
      const { width, height } = action.payload;
      return {
        ...state,
        width,
        height,
      };
  }
  return state;
}
