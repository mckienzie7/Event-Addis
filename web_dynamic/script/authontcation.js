document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('.input-div');
    const emailInput = document.querySelector('.emailinp');
    const passwordInput = document.querySelector('.passwordinp');
    const loginButton = document.querySelector('.sub_login');

    loginButton.addEventListener('click', function(event) {
        event.preventDefault();

        const email = emailInput.value;
        const password = passwordInput.value;

        // Perform basic validation
        if (!email || !password) {
            alert('Please enter both email and password');
            return;
        }

        // Send login request to server
        fetch('http://localhost:5000/api/v1/user/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: email,  // Assuming username is used for login
                password: password
            })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Invalid credentials');
            }
        })
        .then(data => {
            // Assuming server returns an access token upon successful login
            const accessToken = data.access_token;
            // Store the token in local storage or session storage
            localStorage.setItem('accessToken', accessToken);
            // Redirect to dashboard or desired page
            window.location.href = '/dashboard';
        })
        .catch(error => {
            alert(error.message);
        });
    });
});
