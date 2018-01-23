export default class LocalStorageMock {
  constructor() {
    this.store = {};
  }

  clear() {
    this.store = {};
  }

  getItem(key) {
    return this.store[key] || null;
  }

  removeItem(key) {
    delete this.store[key];
  }

  setItem(key, value) {
    this.store[key] = value.toString();
  }
}
