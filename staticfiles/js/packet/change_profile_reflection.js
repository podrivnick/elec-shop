
$('.toggle_btn__profile').on('click', function (e) {
    e.preventDefault();
    var is_packet = $(this).prop('checked');
    let value = $(this).val()

    function updateHTML(is_packet) {
        console.log('df')
        $.ajax({
            type: "POST",
            url: "/users/change_below_profile/",  // Укажите URL для обработки запроса на сервере
            data: {
                is_packet: is_packet,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Заменяем текущий HTML на новый HTML из ответа

                var cartItemsContainer = $("#packet_profile_");
                cartItemsContainer.html(data.carts_items_user);
            },
            error: function (error) {
                console.log("Произошла ошибка при обновлении HTML:", error);
            }
        });
    }

    updateHTML(value);
});
