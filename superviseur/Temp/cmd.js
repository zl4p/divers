"use strict";

// Ajax function pour transfert asynchrone
// url: string
// data: json {name: value}
// callback: function en cas de reussite
function Ajax(url,data={},callback=null) {
  if(typeof(url) !== "string" || typeof(data)!== "object" || (callback!== null && typeof(callback)!== "function")) retunr -1;
  let httpRequest = new XMLHttpRequest();
  console.log(`${url}`);
  httpRequest.open('POST',`${url}`);
  httpRequest.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
  httpRequest.send(JSON.stringify(data));
}

/********************************************
 *  Gestion des commandes show:
 **********************************************/
function CmdShow(str) {
  Ajax('main.html',
  {data: str,ask: 'show'}
  );
}

function CmdAdd(str) {
  console.log("ok add");
}