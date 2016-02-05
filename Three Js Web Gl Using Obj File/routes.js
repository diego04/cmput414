'use strict';

var app = require('./app'),
    route = require('koa-route'),
    render = require('koa-ejs'),
    path = require('path');


render(app, {
    root: path.join(__dirname, 'views'),
    layout: 'layout',
    viewExt: 'html',
    cache: false,
    debug: true
});


app.use(route.get('/', function *() {
    yield this.render('upload', {})

}));

app.use(route.get('/render/:objectname', function *(name) {

    yield this.render('assignment', {
        assignmentpath: name
    })

}));