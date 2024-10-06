
function like(user, id_product, opinion_id, element) {
  let csrftoken = getCookie('csrftoken');

  const data_favorite =  [user, id_product, opinion_id]
  console.log(data_favorite)
  fetch('/carts_products/save_like_opinion/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({data: data_favorite}),

  })
     .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      // Ожидание и возврат JSON из ответа

      return response.json();
    })
    .then(data => {
      // Обработка JSON-данных
      let siblingElement = element.nextElementSibling;
      if (siblingElement.innerText < data.likes_count) {
        element.style.color = "red";
      } else {
        element.style.color = "black";
      }
      setTimeout(function (){
        siblingElement.innerText = data.likes_count;
      }, 120)
    })
    .catch(error => {
      console.error('Ошибка сохранения данных:', error);
    });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      // Ищем cookie с указанным именем
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
