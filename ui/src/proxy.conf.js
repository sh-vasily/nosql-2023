const PROXY_CONFIG = [
  {
    context: [
      "/",
    ],
    target: "http://localhost:8000",
    secure: false,
  }
]

module.exports = PROXY_CONFIG;
