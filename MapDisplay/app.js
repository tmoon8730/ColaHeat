var express = require("express");
var app = express();
var router = express.Router();
var path = __dirname + '/views/';
var path2 = require("path");

var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";

app.use(express.static(path2.join(__dirname, 'public')));

router.use(function (req,res,next) {
  console.log("/" + req.method);
  next();
});

router.get("/",function(req,res){
  res.sendFile(path + "index.html");
});

router.get("/about",function(req,res){
  res.sendFile(path + "about.html");
});

router.get('/api/coordinates',function(req,res){
  MongoClient.connect(url, function(err, db) {
    if (err) throw err;
    var dbo = db.db("ColaHeat");
    dbo.collection("data").findOne({}, function(err, result) {
      if (err) throw err;
      console.log(result);
      res.send(result);
      db.close();
    });
  });
})

app.use("/",router);

app.listen(3000,function(){
  console.log("Live at Port 3000");
});
