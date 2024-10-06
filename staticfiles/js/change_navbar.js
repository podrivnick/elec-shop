$(document).ready(function() {
    var image_packet__black = "{% static 'icons/free-icon-shopping-cart-of-checkered-design-34627.png' %}";
    var image_packet__white = "{% static 'icons/white_packet.png' %}";

    if ($(window).width() <= 768) {
        $(".img_packet__navbar").attr("srcset", image_packet__black);
        $(".show_only_mobile").removeClass('dis_none')
    } else {
        $(".img_packet__navbar").attr("srcset", image_packet__white);
    }
});
