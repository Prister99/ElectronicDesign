const { poll, Client } = require("pg");
const dgram = require('dgram')
const server = dgram.createSocket('udp4')


const connectionString = "postgressql://Taxictrl:Argonauta99@database-1.citbdsotwjsu.us-east-1.rds.amazonaws.com:5432/Taxictrl";
const pgconnection = new Client({
    connectionString: connectionString
});

pgconnection.connect(function(err){
    if(err){
        console.log(err)
    }else{
        console.log('DB connected')
    }
})


    server.on('error',(error)=>{
    console.log('error on the server \n' +error.message)
    server.close()
    })
    
    server.on('listening', ()=>{
        const address = server.address()
        console.log(`server is listening on ${address.address}:${address.port}`)
    })
    
    server.on('message',async(data, rinfo)=>{
        console.log(`server got ${data} from ${rinfo.address}:${rinfo.port}`)
        try{
        await pgconnection.query(`INSERT INTO "Coordenadas"("Longitud","Latitud","Timestamp")VALUES(${data});`, (err,rows,fields)=>{
            if(err){
            console.log(err)
        }else{
           } 
        })}catch(err){
            return next(err)
        }
    })

    server.bind(13550)


module.exports = pgconnection