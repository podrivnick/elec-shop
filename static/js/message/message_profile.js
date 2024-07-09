"use strict"

let block_succesful_message = document.querySelector('.messages_login_registration_position')
let btn_close_seccessful_message = document.querySelector('.close_message_success_btn')

if (block_succesful_message) {
    btn_close_seccessful_message.addEventListener("click", function (e){
        block_succesful_message.classList.add('dis_none')
    });
    setTimeout(function (){
        block_succesful_message.classList.add('dis_none')
    }, 7000)
}