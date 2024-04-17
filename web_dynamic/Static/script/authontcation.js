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
            url: 'http://localhost:5000/api/v1/user/loginn',
            contentType: 'application/json',
            data: JSON.stringify({
                username: username,
                password: password
            }),
            success: function(data) {
                console.log(data);
                // Assuming server returns an access token upon successful login
                const accessToken = data.access_token;
                const role = data.user_info.Role.toLowerCase(); // Ensure lowercase for consistent comparison
                const user_info = JSON.stringify(data.user_info); // Store user_info as a string

                // Store the token and user info in local storage
                localStorage.setItem('accessToken', accessToken);
                localStorage.setItem('Role', role);
                localStorage.setItem('user_info', user_info);

                // Redirect based on role
                if (role === 'administrator') {
                    window.location.href = '../templates/home.html';
                } else if (role === 'organizer') {
                    window.location.href = 'organizer.html';
                } else if (role === 'attendee') {
                    window.location.href = 'home.html'; // Adjust the URL as needed
                } else {
                    throw new Error('Unknown role: ' + role);
                }
            },
            error: function(xhr, status, error) {
                // Handle error response
                alert('Invalid credentials');
            }
        });
    });
});
