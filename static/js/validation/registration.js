document.getElementById('btn_submit_form_registration').addEventListener('click', function(event) {
    var name = document.getElementById('id_username').value;
    var email = document.getElementById('id_email').value;
    var password1 = document.getElementById('id_password1').value;
    var password2 = document.getElementById('id_password2').value;
    var first_name = document.getElementById('id_first_name').value;
    var last_name = document.getElementById('id_last_name').value;

    if (name.trim() === '' || email.trim() === '' || password1.trim() === '' || first_name.trim() === '' || last_name.trim() === '' || password2.trim() === '') {
        alert('Please fill in all fields');
        event.preventDefault();
    }

    if (!isValidEmail(email)) {
        alert('Please enter a valid email address');
        event.preventDefault();
    }

    if (!isValidPassword(password1)) {
        alert('Please enter a password with at least 8 characters');
        event.preventDefault();
    }
    if (isEqualPasswords(password1, password2)){
        alert('Please enter a equal passwords');
        event.preventDefault();
    }
});

function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPassword(password) {
    return password.length >= 8;
}

function isEqualPasswords(password1, password2) {
    return password1 !== password2
}