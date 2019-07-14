const https = require('https')
const fs = require('fs')

const options = {
  key: fs.readFileSync('E:/workfiles/Project/ssl/server.key'),
  cert: fs.readFileSync('E:/workfiles/Project/ssl/server.crt')
};
https.createServer(options, function (req, res) {
  setTimeout(() => {
    // res.writeHead(200, { 'Content-Type': 'text/plain' });
    // res.write('request successfully proxied to: ' + req.url + '\n' + JSON.stringify(req.headers, true, 2));
    let html = fs.readFileSync('./imgCaptcha.htm')
    res.end(html);
  }, 10 * 1000)
}).listen(9008);
