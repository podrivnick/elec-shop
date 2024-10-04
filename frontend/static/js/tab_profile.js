

let btn_first_tab = document.querySelector('.btn_tab_profile1')
let btn_second_tab = document.querySelector('.btn_tab_profile2')
let btn_third_tab = document.querySelector('.btn_tab_profile3')
let block_main_tab = document.querySelectorAll('.chenger_reflections_products')


if (block_main_tab){
    btn_first_tab.addEventListener("click", function (e){
        if (block_main_tab[0].classList.contains('taken')){
            //
        }
        block_main_tab[0].classList.add('taken')
        block_main_tab[1].classList.remove('taken')
        block_main_tab[2].classList.remove('taken')
    });
    btn_second_tab.addEventListener("click", function (e){
        if (block_main_tab[1].classList.contains('taken')){
            //
        }
        block_main_tab[1].classList.add('taken')
        block_main_tab[0].classList.remove('taken')
        block_main_tab[2].classList.remove('taken')
    });
    btn_third_tab.addEventListener("click", function (e){
        if (block_main_tab[2].classList.contains('taken')){
            //
        }
        block_main_tab[2].classList.add('taken')
        block_main_tab[1].classList.remove('taken')
        block_main_tab[0].classList.remove('taken')
    });
}
