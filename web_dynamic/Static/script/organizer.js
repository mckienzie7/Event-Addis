document.addEventListener("DOMContentLoaded", function() {
        // Check if there's an access token and username
        const session_id = localStorage.getItem('session_id');
        const username = localStorage.getItem('username');

        if (session_id) {
                // Check if the success message has already been shown in this session
                const successMessageShown = sessionStorage.getItem('successMessageShown');

                if (!successMessageShown) {
                        // Create a success message element
                        const successMessage = document.createElement('div');
                        successMessage.className = 'success-message';
                        successMessage.textContent = 'Successful!';
                        document.body.appendChild(successMessage);

                        // Set timeout to remove the success message after 4 seconds
                        setTimeout(function() {
                                successMessage.remove();
                                sessionStorage.setItem('successMessageShown', 'true'); // Set flag to indicate success message has been shown in this session
                        }, 4000);
                }

                // Greet the user if username exists
                if (username) {
                        document.querySelector('.greet-user p').textContent = 'Oh hello, ' + username + '!';
                        document.querySelector('.two p').textContent = username;
                }

                // Logout functionality
                const logoutButton = document.querySelector('.logout');
                logoutButton.addEventListener('click', function() {
                        // Create and display a confirmation message
                        const confirmationMessage = document.createElement('div');
                        confirmationMessage.className = 'confirmation-message';
                        confirmationMessage.innerHTML = 'Are you sure you want to logout?<br><button class="confirm-logout" id="yes">Yes</button><button class="cancel-logout" id="no">No</button>';
                        document.body.appendChild(confirmationMessage);

                        // Show confirmation dialog
                        confirmationMessage.style.display = 'block';

                        // Handle confirm logout button click
                        document.getElementById('yes').addEventListener('click', function() {
                                // Send logout request to the server
                                fetch('http://localhost:5000/api/v1/users/logout', {
                                        method: 'DELETE',
                                        credentials: 'include',  // This includes cookies in the request
                                        headers: {
                                                'Content-Type': 'application/json'
                                        }
                                })
                                    .then(response => {
                                            if (response.ok) {
                                                    window.location.href = 'login.html';
                                                    // Clear local storage and redirect to login page
                                                    localStorage.clear();
                                            } else {
                                                    alert('Failed to log out. Please try again.');
                                            }
                                    })
                                    .catch(error => console.error('Error logging out:', error));
                        });

                        // Handle cancel logout button click
                        document.getElementById('no').addEventListener('click', function() {
                                confirmationMessage.style.display = 'none';
                        });
                });
        } else {
                // Redirect to login page if not authenticated
                window.location.href = 'login.html';
        }
});
