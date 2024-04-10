document.addEventListener('DOMContentLoaded', function() {
        // Check if role is organizer or administrator
        var role = localStorage.getItem('Role');

        if (role === 'organizer' || role === 'administrator') {
                // Create a success message element
                var successMessage = document.createElement('div');
                successMessage.className = 'success-message';
                successMessage.textContent = 'Login successful!'; // You can customize this message

                // Append the success message to the body
                document.body.appendChild(successMessage);

                // Set timeout to remove the success message after 10 seconds
                setTimeout(function() {
                        successMessage.remove();
                }, 4000); // 10 seconds (10,000 milliseconds)
        }
});

