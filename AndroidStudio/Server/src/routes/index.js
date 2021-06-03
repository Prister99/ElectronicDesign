const { json } = require('express')
const express = require('express')
const pgconnection = require('./database-udpserver')
const router = express.Router()

router.get('/',(req,res)=>{
    res.render('index.html',{title: 'Taxi control'})
})

router.get('/history',(req,res)=>{
    res.render('history.html',{title: 'History'})
})

router.get('/place_history',(req,res)=>{
    res.render('place.html',{title: 'Place History'})
})

router.get('/api/live',async(req,res)=>{
    try{
    pgconnection.query('SELECT "Longitud","Latitud","Timestamp" FROM "Coordenadas" order by id desc limit 1', async(err, rows, fields) => {
        try{
            if (!err) {
                res.json(rows)
                let data = res.json(rows)
                console.log(data)
            } else {
                console.log(err)
            }
            return data.json()
        }catch{(err)=> console.log(err)
        }
        })
}catch{(err)=> console.log(err)
}
})

router.get('/api/:id',(req,res)=>{
    try{
        var {id} = req.params
        id = id.split(";")
        const start = id[0].split("T").join(" ")
        const end = id[1].split("T").join(" ")

        pgconnection.query(`SELECT * FROM "Coordenadas" WHERE "Timestamp" >=\'${start}\' AND "Timestamp"<=\'${end}\';`, async(err, rows, fields) => {
            try{
                if (!err) {
                    res.json(rows)             
                } else {
                    console.log(err)
                }
            }catch{(err)=> console.log(err)
            }
            })
    }catch{(err)=> console.log(err)
    }
    })

    router.get('/api/place/:id',(req,res)=>{
        try{
            var {id} = req.params
            id = id.split(";")
            const start = id[0] //.split("T").join(" ")
            const end = id[1] //.split("T").join(" ")
            const start2 = id[2] //.split("T").join(" ")
            const end2 = id[3] //.split("T").join(" ")

            pgconnection.query(`SELECT * FROM "Coordenadas" WHERE "Longitud" >=\'${start}\' AND "Longitud" <=\'${end}\' AND "Latitud">=\'${start2}\' AND "Latitud"<=\'${end2}\';`, async(err, rows, fields) => {
                try{
                    if (!err) {
                        res.json(rows)             
                    } else {
                        console.log(err)
                    }
                }catch{(err)=> console.log(err)
                }
                })
        }catch{(err)=> console.log(err)
        }
        })

module.exports = router