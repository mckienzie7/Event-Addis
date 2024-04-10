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
                console.log(data)
                // Assuming server returns an access token upon successful login
                const accessToken = data.access_token;
                const Role = data.user_info.Role
                const user_info = data.user_info

                // Store the token in local storage
                localStorage.setItem('accessToken', accessToken);
                localStorage.setItem('Role', Role);
                localStorage.setItem('user_info', user_info)
                // Redirect based on role
                if (Role === 'Adminstrator') {
                    window.location.href = '../templates/home.html';
                } else if (Role === 'organizer') {
                    window.location.href = 'organizer.html';
                } else if (Role === 'Attendee') {
                    window.location.href = '/home';
                } else {
                    throw new Error('Unknown role');
                }
            },
            error: function(xhr, status, error) {
                // Handle error response
                alert('Invalid credentials');
            }
        });
    });
});
