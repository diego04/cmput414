'use strict';


var logger = require('koa-logger');
var serve = require('koa-static');
var parse = require('co-busboy');
var koa = require('koa');
var fs = require('fs');
var app = module.exports = koa();
var os = require('os');
var path = require('path');
var mount = require('koa-mount');



var cors = require('koa-cors');
app.use(cors());


// log requests

app.use(logger());

// custom 404

app.use(function *(next){
    yield next;
    if (this.body || !this.idempotent) return;
    this.redirect('/public/404.html');
});

// serve files from ./public

app.use(mount('/public',serve(__dirname + '/public')));

// handle uploads

app.use(function *(next){
    // ignore non-POSTs
    if ('POST' != this.method) return yield next;

    // multipart upload
    var parts = parse(this);
    var part;

    var filename = ''

    while (part = yield parts) {
        console.log(os.tmpdir())
        //var stream = fs.createWriteStream(path.join(os.tmpdir(), Math.random().toString()));
        var stream = fs.createWriteStream(__dirname + '/public/' + part.filename);

        //var stream = fs.createWriteStream(path.join(os.tmpdir(), Math.random().toString()));
        part.pipe(stream);
        console.log('uploading %s -> %s', part.filename, stream.path);

        filename = part.filename
        console.log(part.filename)
    }

    this.redirect('/render/'+filename);
});

// listen

require('./routes.js');


var port = process.env.PORT || 8000
app.listen(port);
console.log('listening on port 8000');