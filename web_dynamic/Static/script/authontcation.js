$(document).ready(function() {
    // Selecting elements from the DOM
    const emailInput = $('.emailinp');
    const passwordInput = $('.passwordinp');
    const loginButton = $('.sub_login');

    // Adding click event listener to the login button
    loginButton.on('click', function(event) {
        event.preventDefault();

        // Retrieving values of email and password inputs
        const username = emailInput.val();
        const password = passwordInput.val();

        // Performing basic validation
        if (!username || !password) {
            alert('Please enter both email and password');
            return;
        }

        // Sending login request to server using AJAX
        $.ajax({
            type: 'POST',
            url: 'http://localhost:5000/api/v1/users/login',
            contentType: 'application/json',
            data: JSON.stringify({
                username: username,
                password: password
            }),
            success: function(data) {
                console.log(data);
                const email = data.email;  // The email from server response
                const message = data.message;  // Success message: "logged in"

            },
            error: function(xhr, status, error) {
                // Handle error response
                alert('Invalid credentials');
            }
        });
    });
});
