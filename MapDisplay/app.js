var express = require("express");
var app = express();
var router = express.Router();
var path = __dirname + '/views/';
var path2 = require("path");

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

app.use("/",router);

app.listen(3000,function(){
  console.log("Live at Port 3000");
});
