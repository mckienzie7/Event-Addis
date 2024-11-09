// Wait for the DOM content to be fully loaded before executing JavaScript code
document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to an element with class 'sub_login'
    const subLoginButton = document.querySelector('.sub_login');
    if (subLoginButton) { // Check if the button exists
        subLoginButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default form submission behavior

            // Retrieve form input values
            const emailInput = document.querySelector('input[name="email"]');
            const confirmEmailInput = document.querySelector('input[name="confirm_email"]');
            const usernameInput = document.querySelector('input[name="username"]');
            const passwordInput = document.querySelector('input[name="password"]');

            // Check if inputs exist
            if (!emailInput || !confirmEmailInput || !usernameInput || !passwordInput) {
                console.error('One or more form inputs are missing');
                return;
            }

            // Retrieve input values
            const email = emailInput.value;
            const confirmEmail = confirmEmailInput.value;
            const username = usernameInput.value;
            const password = passwordInput.value;
            const admin = false;

            // Regular expression to validate email format
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            // Validate email format
            if (!emailRegex.test(email)) {
                alert('Invalid email address');
                return;
            }

            // Check if email and confirm email match
            if (email !== confirmEmail) {
                alert('Emails do not match');
                return;
            }

            // Construct user object
            const newUser = {
                email: email,
                username: username,
                password: password,
                admin: admin,
            };

            // Send POST request to server to register user
            fetch('http://localhost:5000/api/v1/users/Register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newUser),
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    }
                    throw new Error('Network response was not ok.');
                })
                .then(data => {
                    console.log('Registration successful:', data);
                    // Handle success response
                    window.location.href = 'login.html';
                    alert('User registered successfully');
                    // Redirect to login
                     // Adjust this path if necessary
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                    // Handle error
                    alert('Failed to register user');
                });
        });
    } else {
        console.error('Button with class "sub_login" not found');
    }
});
