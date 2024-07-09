document.getElementById('login_form_submit').addEventListener('click', function(event) {
    var name = document.getElementById('id_username').value;
    var email = document.getElementById('id_email').value;
    var password = document.getElementById('id_password').value;

    if (name.trim() === '' || email.trim() === '' || password.trim() === '') {
        alert('Please fill in all fields');
        event.preventDefault();
    }

    if (!isValidEmail(email)) {
        alert('Please enter a valid email address');
        event.preventDefault();
    }

    if (!isValidPassword(password)) {
        alert('Please enter a password with at least 8 characters');
        event.preventDefault();
    }
});

function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPassword(password) {
    return password.length >= 4;
}