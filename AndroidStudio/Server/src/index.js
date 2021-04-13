const express = require('express')
const app = express()
const path = require('path')


// procces.env.PORT ||

// settings
app.set('port', 13555)
app.set('view engine', 'ejs')
app.set('json spaces',2)
app.set('views',path.join(__dirname, 'views'))
app.engine('html', require('ejs').renderFile)

//middlewares

//routes
app.use(require('./routes/index'))
//static files

//listener the sever
app.listen(app.get('port'),()=>{
console.log('Server on port: '+ app.get('port'))

});
