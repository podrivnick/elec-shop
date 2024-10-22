$(document).ready(function () {
  $(document).on("click", ".btn_delete_opinion", function (e) {
    e.preventDefault();

    confirm_delete_opinion = $('.block_modal_popup_delete_opinion').first()
    if (confirm_delete_opinion && $(confirm_delete_opinion).hasClass("dis_none")) {
      $(confirm_delete_opinion).removeClass("dis_none");
    }
  });

  // Обработчик для кнопки закрытия
  $(document).on("click", ".close_popup_confirm_opinion_delete", function (e) {
    e.preventDefault();
    $(confirm_delete_opinion).addClass("dis_none");
  });

  // Обработчик для кнопки подтверждения удаления
  $(document).on("click", ".sure_delete_opinion", function (e) {
    let product_slug = $(this).data("product-slug");
    let product_pk = $(this).data("product-pk");
    console.log(product_pk)
    e.preventDefault();
    $(confirm_delete_opinion).addClass("dis_none");

    $.ajax({
      type: "POST",
      url: '/api/v1/cart/reviews/delete_reveiw/',
      data: {
        product_pk: product_pk,
        product_slug: product_slug,
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
      },
      success: function (data) {
        location.reload();
      },
      error: function (data) {
        console.log("Ошибка при добавлении товара в корзину");
      },
    });
  });
});
