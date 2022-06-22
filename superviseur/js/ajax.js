"use strict";

// Ajax function pour transfert asynchrone
// url: string
// data: json {name: value}
// callback: function en cas de reussite
function Ajax(url,data,callback=null) {
    //if(typeof(url) !== "string" || typeof(data)!== "object" || (callback!== null && typeof(callback)!== "function")) return -1;
    let httpRequest = new XMLHttpRequest();
  
    httpRequest.open('POST',`${url}`);
    httpRequest.setRequestHeader("Accept", "application/json");
    httpRequest.setRequestHeader("Content-Type", "application/json");
//    httpRequest.setRequestHeader('Content-type',"text/plain; charset=UTF-8");
    httpRequest.send(JSON.stringify(data));
    httpRequest.addEventListener('readystatechange',function(data) {
      if(this.status === 200 && this.readyState === XMLHttpRequest.DONE)
        callback(this.responseText);
    })
  }
  

