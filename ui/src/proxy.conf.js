const PROXY_CONFIG = [
  {
    context: [
      "/",
    ],
    target: "http://localhost",
    secure: false,
  }
]

module.exports = PROXY_CONFIG;
