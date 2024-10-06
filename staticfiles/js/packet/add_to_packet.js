// Добавляем товар в корзину, удаляем и изменяем количество товаров в корзине
$(document).ready(function () {
   function initCloseModalButton() {
    let modal_popup_window = document.querySelector('.container_modal_popup_packet');
    let close_modal_popup_packet = document.querySelector('.close_popup_packet_btn');

    if (close_modal_popup_packet) {
      close_modal_popup_packet.addEventListener("click", function (e) {
        modal_popup_window.classList.remove('open');
      });
    }
   }
  function initAddToCartButton() {
    // Ловим событие клика по кнопке добавить в корзину
    $(document).on("click", ".add_packet_product", function (e) {
      e.preventDefault();

      let product_id = $(this).data("product-id");

      let total_price_all_packet = $('#total_price_all_packet')
      let cartCount = parseInt(total_price_all_packet.text() || 0);

      $.ajax({
        type: "POST",
        url: '/packet/save_product_packet/',
        data: {
          product_id: product_id,
          csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        },
        success: function (data) {
          // Выводим сообщение об успешном добавлении товара в корзину
          success_message = document.querySelector('.added_packet')
          if (success_message && success_message.classList.contains('dis_none') && data.message){
            success_message.classList.remove('dis_none')
            setTimeout(function (e){
              success_message.classList.add('dis_none')
            }, 4700)
          }
          cartCount++;
          total_price_all_packet.text(cartCount);

          // Обновляем содержимое корзины
          var cartItemsContainer = $("#modal_packet_popup");
          cartItemsContainer.html(data.carts_items_user);

          // Повторно инициализируем обработчик событий на кнопке добавить в корзину
          initCloseModalButton();
        },
        error: function (data) {
          console.log("Ошибка при добавлении товара в корзину");
        },
      });
    });
  }

  // Инициализируем обработчик событий на кнопке добавить в корзину
  initAddToCartButton();

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
          cart_id: cart_id,
          is_profile: false,
          csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        },
        success: function (data) {
          // Выводим сообщение об успешном добавлении товара в корзину
            console.log(data.new_quantity)
          cartCount = data.new_quantity;
          total_price_all_packet.text(cartCount);

          // Обновляем содержимое корзины
          var cartItemsContainer = $("#modal_packet_popup");
          cartItemsContainer.html(data.carts_items_user);

          // Повторно инициализируем обработчик событий на кнопке добавить в корзину
          initCloseModalButton();
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
          cart_id: cart_id,
          is_profile: false,
          is_plus: is_plus,
          csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        },
        success: function (data) {
          // Выводим сообщение об успешном добавлении товара в корзину
            console.log(data.new_quantity)

          cartCount = data.new_quantity;
          total_price_all_packet.text(cartCount);

          // Обновляем содержимое корзины
          var cartItemsContainer = $("#modal_packet_popup");
          cartItemsContainer.html(data.carts_items_user);

          // Повторно инициализируем обработчик событий на кнопке добавить в корзину
          initCloseModalButton();
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
          is_profile: false,
          is_plus: is_plus,
          cart_id: cart_id,
          csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        },
        success: function (data) {
          cartCount = data.new_quantity;
          total_price_all_packet.text(cartCount);

          // Обновляем содержимое корзины
          var cartItemsContainer = $("#modal_packet_popup");
          cartItemsContainer.html(data.carts_items_user);

          // Повторно инициализируем обработчик событий на кнопке добавить в корзину
          initCloseModalButton();
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
