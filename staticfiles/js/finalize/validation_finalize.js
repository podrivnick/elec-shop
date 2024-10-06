document.getElementById("order_cart_finalize").addEventListener("click", function(event) {
    event.preventDefault();

    var email = document.getElementById("id_email_finalize");
    var phone = document.getElementById("id_phone_finalize");
    var address = document.getElementById("id_address_finalize");
    var name = document.getElementById("id_name_finalize");
    var surname = document.getElementById("id_surname_finalize");

    var phonePattern = /^\+\d{6,}$/;
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email.value)) {
        email.classList.add('invalid')
        event.preventDefault();
        return;
    } else {
        if (email.classList.contains('invalid')) {
           email.classList.remove('invalid');
        }
    }

    if (!phonePattern.test(phone.value.replace(/\s/g, ''))) {
        phone.classList.add('invalid');
        event.preventDefault();
        return;
    } else {
        if (phone.classList.contains('invalid')) {
            phone.classList.remove('invalid');
        }
    }

    if (address.value.length > 0 && address.value.length < 10) {
        alert("Адрес должен содержать не менее 10 символов");
        event.preventDefault();
        return;
    }
    if (!surname.value) {
        if (!surname.classList.contains('invalid')) {
            surname.classList.add('invalid')
        }
    } else {
        if (surname.classList.contains('invalid')) {
            surname.classList.remove('invalid')
        }
    }

    if (!name.value) {
        if (!name.classList.contains('invalid')) {
            name.classList.add('invalid')
        }
    } else {
        if (name.classList.contains('invalid')) {
            name.classList.remove('invalid')
        }
    }

    if (name.value && surname.value) {
        document.getElementById("form_finalize_product_").submit();
    }
});
