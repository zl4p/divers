"use strict";

// [+] Gestion de l'identification
((function(){

    let btn_ident = document.querySelector("#identification")
    btn_ident.addEventListener("submit",(e,ev) => {
        e.preventDefault(); // Stop la propagation
        let l= document.getElementsByName("login")[0].value || ""
        let p = document.getElementsByName("pass")[0].value || ""
        Ajax("/ident",{"login":l,"pass":p},function(t){
            console.log(t)
            if("succes" == t) {
                console.log("ok")
            }
            else {
                console.log("nok")
            }
        });
        return false;

    })
}))();


function ShowAlertMsg(msg) {

}