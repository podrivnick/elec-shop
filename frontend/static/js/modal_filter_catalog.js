
let popup_catalog_btn = document.querySelector('.catalog_btn')
let popup_catalog = document.querySelector('.main_catalog_form')


if (popup_catalog) {
    popup_catalog_btn.addEventListener("click", function (e){
        popup_catalog.classList.toggle('visible_popup_catalog')
    });
}

let popup_filters_btn = document.querySelector('.btn-filter')
let popup_filters = document.querySelector('.container_filters')

if (popup_filters_btn) {
    popup_filters_btn.addEventListener("click", function (e){
        popup_filters.classList.remove("visible_popup_catalog")
    })
}

let close_popup_filters = document.querySelector('.close_filters_btn');

if (close_popup_filters) {
    close_popup_filters.addEventListener("click", function (e){
        popup_filters.classList.add('visible_popup_catalog')
    })
}

let packet_popup_modal_img = document.querySelector('.packet_btn')
let modal_popup_window = document.querySelector('.container_modal_popup_packet')

if (packet_popup_modal_img){
    packet_popup_modal_img.addEventListener("click", function (e){
        modal_popup_window.classList.add('open')
    });
}
let close_modal_popup_packet = document.querySelector('.close_popup_packet_btn')

if (close_modal_popup_packet){
    close_modal_popup_packet.addEventListener("click", function (e){
        modal_popup_window.classList.remove('open')
    });
}
