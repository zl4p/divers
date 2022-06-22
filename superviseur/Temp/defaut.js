"use strict";

// Ajax function pour transfert asynchrone
// url: string
// data: json {name: value}
// callback: function en cas de reussite
function Ajax(url,data,callback=null) {
  if(typeof(url) !== "string" || typeof(data)!== "object" || (callback!== null && typeof(callback)!== "function")) retunr -1;
  let httpRequest = new XMLHttpRequest();
  xhr.setRequestHeader("Accept", "application/json");
  xhr.setRequestHeader("Content-Type", "application/json");
  httpRequest.open('POST',`${url}`);
  httpRequest.send(data);
  httpRequest.addEventListener('readystatechange',function(data) {
    if(this.status === 200 && this.readyState === XMLHttpRequest.DONE)
      callback(this.responseText);
  })
}

let req = document.getElementById("requeteur") || null;
if (req !== null) {
  req.addEventListener('submit',function(e) {
    e.preventDefault();
    let req = document.getElementById("val_requeteur").value;
    req = req.replace(/(^\s+)|(\s+)$/gi,'').replace(/\s{2,}/gi,' ');
    Ajax("main.html",req,UpdateViewer);
  });
}
function UpdateViewer(data) {
  data = JSON.parse(data).data;
  let viewer = document.getElementById('viewer');
  let info = null;
  for(let a in data) {
    info = document.createElement("div");
    info.className = 'row';
    info.innerHTML = `<strong> ${data[a].title} </strong> ${data[a].content}`;
    viewer.insertBefore(info,viewer.firstChild);
  }

}
