$(document).ready(function() {
        // Check if there's an access token and user role
        const session_id = localStorage.getItem('session_id')

        // Check if the access token and role are valid
        if (session_id) {
                // Check if the success message has already been shown in this session
                var successMessageShown = sessionStorage.getItem('successMessageShown');

                if (!successMessageShown) {
                        // Create a success message element
                        var successMessage = $('<div class="success-message">Successful!</div>');

                        // Append the success message to the body
                        $('body').append(successMessage);

                        // Set timeout to remove the success message after 4 seconds (4000 milliseconds)
                        setTimeout(function() {
                                successMessage.remove();
                                sessionStorage.setItem('successMessageShown', 'true'); // Set flag to indicate success message has been shown in this session
                        }, 4000);
                }

                // Greet the user
                var user_info = JSON.parse(localStorage.getItem('user_info'));
                if (user_info && user_info.username && user_info.fullname) {
                        var fullName = user_info.fullname;
                        var userName = user_info.username;
                        var greetingText = 'Oh hello, ' + fullName + '!';
                        $('.greet-user p').text(greetingText);
                        $('.two p').text(userName);
                }

                // Logout functionality
                const logout = $('.logout');
                logout.click(function (){
                        // Show confirmation message
                        var confirmationMessage = $('<div class="confirmation-message">Are you sure you want to logout?<br><button class="confirm-logout" id="yes">Yes</button><button class="cancel-logout" id="no">No</button></div>');
                        $('body').append(confirmationMessage);

                        // Handle confirm logout button click
                        $('.logout').click(function() {
                                $('.confirmation-message').fadeIn();
                        });

                        $('.confirm-logout').click(function() {
                                localStorage.clear();
                                window.location.href = 'login.html';
                        });

                        $('.cancel-logout').click(function() {
                                $('.confirmation-message').fadeOut();
                        });
                });
        } else {
                // Redirect to login page or handle unauthorized access
                window.location.href = 'login.html'; // Change to your login page URL
        }
});
