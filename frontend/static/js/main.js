"use strict"

// Equip system user work at
const isMobile = {
    Android: function () {
        return navigator.userAgent.match(/Android/i);
    },
    BlackBerry: function () {
        return navigator.userAgent.match(/BlackBerry/i);
    },
    iOS: function () {
        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
    },
    Opera: function () {
        return navigator.userAgent.match(/Opera Mini/i);
    },
    Windows: function () {
        return navigator.userAgent.match(/IEMobile/i);
    },
    any: function () {
        return (
            isMobile.Android() ||
            isMobile.BlackBerry() ||
            isMobile.iOS() ||
            isMobile.Opera() ||
            isMobile.Windows());
    },
}

// add to body identificator of system user work at
// add to last .link-light .__active_arrow if .navbar__arrow has clicked (delete that if double click)
if (isMobile.any()) {
    document.body.classList.add('_touch');
}else{
    document.body.classList.add('_pс');
}

// burger icon
const icon_menu_burger = document.querySelector('.menu_icon');

// add to body ._lock after clicked (delete that if double click)
// add to burger .__active_burger
// add .__active_burger for create new background settings while burger active
if (icon_menu_burger) {
    const menu_body = document.querySelector('.navbar-header')

    icon_menu_burger.addEventListener('click', function (e){
        document.body.classList.toggle('_lock')
        icon_menu_burger.classList.toggle('__active_burger')
        menu_body.classList.toggle('__active_burger')
    });
}
