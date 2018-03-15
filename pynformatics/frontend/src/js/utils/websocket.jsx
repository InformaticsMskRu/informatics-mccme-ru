import ReconnectingWebsocket from 'reconnecting-websocket';


export default class Socket {
  constructor(url, dispatch) {
    this.socket = new ReconnectingWebsocket(url);
    this.socket.addEventListener('open', event => this.onOpen(event));
    this.socket.addEventListener('message', event => this.onMessage(event));

    this.dispatch = dispatch;
  }

  onOpen(event) {
  }

  onMessage(event) {
    this.dispatch({
      type: 'WEBSOCKET_MESSAGE',
      data: JSON.parse(event.data),
    })
  }
}
