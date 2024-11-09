document.addEventListener('DOMContentLoaded', function() {
    const subLoginButton = document.querySelector('.btn'); // Change to .btn
    if (subLoginButton) {
        subLoginButton.addEventListener('click', function(event) {
            event.preventDefault();

            const emailInput = document.querySelector('input[name="email"]');
            const confirmEmailInput = document.querySelector('input[name="confirm-email"]'); // Fix the name to match HTML
            const usernameInput = document.querySelector('input[name="username"]');
            const passwordInput = document.querySelector('input[name="password"]');
            const confirmPasswordInput = document.querySelector('input[name="confirm-password"]'); // Fix the name to match HTML

            if (!emailInput || !confirmEmailInput || !usernameInput || !passwordInput || !confirmPasswordInput) {
                console.error('One or more form inputs are missing');
                return;
            }

            const email = emailInput.value;
            const confirmEmail = confirmEmailInput.value;
            const username = usernameInput.value;
            const password = passwordInput.value;
            const admin = true;  // Always set admin to true

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!emailRegex.test(email)) {
                alert('Invalid email address');
                return;
            }

            if (email !== confirmEmail) {
                alert('Emails do not match');
                return;
            }

            if (password !== confirmPasswordInput.value) {
                alert('Passwords do not match');
                return;
            }

            const newUser = {
                email: email,
                username: username,
                password: password,
                admin: admin,  // admin is always true
            };

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
                    window.location.href = 'login.html';
                    alert('User registered successfully');
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                    alert('Failed to register user');
                });
        });
    } else {
        console.error('Button with class "btn" not found');
    }
});
