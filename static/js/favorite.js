

function favorite_data(user, product) {

  let csrftoken = getCookie('csrftoken');

  const data_favorite =  [user, product]
  console.log(data_favorite)
  fetch('/save_favorite', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ data: data_favorite }),

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
      console.log(data);
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


var btn_heart_favorite = document.querySelectorAll('.btn_heart_favorite');

for (let i = 0; i < btn_heart_favorite.length; i++) {
  btn_heart_favorite[i].addEventListener("click", function (e) {
    var currentButton = e.target;
    if (currentButton.style.color === "red") {
      currentButton.style.color = "black";
    } else {
      currentButton.style.color = "red";
    }
  });
}