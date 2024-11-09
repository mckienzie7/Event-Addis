document.addEventListener('DOMContentLoaded', function () {
    // Get the login button and add an event listener
    const loginButton = document.querySelector('.sub_login');
    if (loginButton) {
        loginButton.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the default form submission behavior

            // Retrieve the input values
            const emailInput = document.querySelector('input[name="email"]');
            const passwordInput = document.querySelector('input[name="password"]');

            // Validate that both inputs exist and have values
            if (!emailInput || !passwordInput || !emailInput.value || !passwordInput.value) {
                alert("Please enter both email and password.");
                return;
            }

            const email = emailInput.value;
            const password = passwordInput.value;

            // Prepare the data to be sent to the server
            const loginData = {
                email: email,
                password: password
            };

            // Send the POST request to login the user
            fetch('http://localhost:5000/api/v1/users/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginData)
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Invalid credentials');
                }
            })
            .then(data => {

                // Check if the user is an admin
                if (data.admin === true) {
                    // Redirect to the admin dashboard if admin is true
                    localStorage.setItem('admin', true); // Store admin status
                    window.location.href = 'admindashboard.html'; // Redirect to admin dashboard
                } else {
                    localStorage.setItem('username', data.username);  // Correct usage of JSON.stringify
                    localStorage.setItem('session_id', data.session_id); // Save session ID
                    localStorage.setItem('email', data.email); // Save email
                    localStorage.setItem('user_id', data.user_id); // Save user ID
                    window.location.href = 'home.html'; // Redirect to home page
                }

                // Store additional details in localStorage if needed
                alert('Login successful');
            })
            .catch(error => {
                console.error('Login error:', error);
                alert('Login failed. Please check your credentials and try again.');
            });
        });
    } else {
        console.error('Login button not found');
    }
});
