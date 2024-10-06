// Добавляем товар в корзину, удаляем и изменяем количество товаров в корзине профиля
$(document).ready(function () {
  function initDeleteCart() {
     $(document).on("click", ".btn_delete_product_from_packet", function (e) {
        e.preventDefault();

        let cart_id = $(this).data("cart-id");

        let total_price_all_packet = $('#total_price_all_packet')
        let cartCount = parseInt(total_price_all_packet.text() || 0);

        $.ajax({
        type: "POST",
        url: '/packet/delete_cart/',
        data: {
          is_profile: true,
          cart_id: cart_id,
          csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        },
        success: function (data) {
          // Выводим сообщение об успешном добавлении товара в корзину
            console.log(data.new_quantity)
          cartCount = data.new_quantity;
          total_price_all_packet.text(cartCount);

          // Обновляем содержимое корзины
          var cartItemsContainer = $("#packet_profile_");
          cartItemsContainer.html(data.carts_items_user);

        },
        error: function (data) {
          console.log("Ошибка при удалении товара из корзины");
        },
      });
     })
  }

  // Инициализируем обработчик событий на кнопке удалить из корзины
  initDeleteCart();
  function initUpdateCartPlus() {
     $(document).on("click", ".btn_plus", function (e) {
        e.preventDefault();

        let cart_id = $(this).data("cart-id");

        let total_price_all_packet = $('#total_price_all_packet')
        let cartCount = parseInt(total_price_all_packet.text() || 0);

        let is_plus = true

        $.ajax({
        type: "POST",
        url: '/packet/change_count_product/',
        data: {
          is_profile: true,
          cart_id: cart_id,
          is_plus: is_plus,
          csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        },
        success: function (data) {
          // Выводим сообщение об успешном добавлении товара в корзину
            console.log(data.new_quantity)

          cartCount = data.new_quantity;
          total_price_all_packet.text(cartCount);

          // Обновляем содержимое корзины
          var cartItemsContainer = $("#packet_profile_");
          cartItemsContainer.html(data.carts_items_user);
        },
        error: function (data) {
          console.log("Ошибка при удалении товара из корзины");
        },
      });
     })
  }

  // Инициализируем обработчик событий увеличения количества продуктов
  initUpdateCartPlus()

  function initUpdateCartMinus() {
     $(document).on("click", ".btn_minus", function (e) {
        e.preventDefault();

        let cart_id = $(this).data("cart-id");

        let total_price_all_packet = $('#total_price_all_packet')
        let cartCount = parseInt(total_price_all_packet.text() || 0);

        let is_plus = false

        $.ajax({
        type: "POST",
        url: '/packet/change_count_product/',
        data: {
          is_plus: is_plus,
          is_profile: true,
          cart_id: cart_id,
          csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        },
        success: function (data) {
          // Выводим сообщение об успешном добавлении товара в корзину
            console.log(data.new_quantity)
          cartCount = data.new_quantity;
          total_price_all_packet.text(cartCount);

          // Обновляем содержимое корзины
          var cartItemsContainer = $("#packet_profile_");
          cartItemsContainer.html(data.carts_items_user);

        },
        error: function (data) {
          console.log("Ошибка при удалении товара из корзины");
        },
      });
     })
  }

  // Инициализируем обработчик событий уменьшения количества продуктов
  initUpdateCartMinus()
});
