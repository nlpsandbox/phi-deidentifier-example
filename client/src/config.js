const defaultValues = {
  SERVER_PROTOCOL: "http://",
  SERVER_HOST: "localhost",
  SERVER_PORT: "8080",
  SERVER_API_PATH: "/api/v1"
}

export default class Config {
  constructor() {}

  getProperty(key) {
    if ('REACT_APP_' + key in process.env) {
      return process.env['REACT_APP_' + key];
    } else {
      return defaultValues[key]
    }
  }

  serverProtocol() {
    return this.getProperty('SERVER_PROTOCOL');
  }

  serverHost() {
    return this.getProperty('SERVER_HOST');
  }

  serverPort() {
    return this.getProperty('SERVER_PORT');
  }

  serverUrl() {
    const serverProtocol = this.serverProtocol();
    const serverHost = this.serverHost();
    const serverPort = this.serverPort();
    return `${serverProtocol}${serverHost}:${serverPort}`
  }

  serverApiPath() {
    return this.getProperty('SERVER_API_PATH');
  }

  serverApiUrl() {
    const serverUrl = this.serverUrl();
    const serverApiPath = this.serverApiPath();
    return `${serverUrl}${serverApiPath}`;
  }

}