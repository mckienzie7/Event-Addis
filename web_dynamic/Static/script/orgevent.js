document.addEventListener('DOMContentLoaded', function() {
    // Function to retrieve session ID and user info from localStorage
    const sessionId = localStorage.getItem('session_id');  // Get session ID from localStorage
    const username = localStorage.getItem('username')?.slice(0, 2).toUpperCase();  // Safely accessing the username
    const email = localStorage.getItem('email')?.slice(0, 8);  // Safely accessing the email
    const user_id = localStorage.getItem('user_id');

    if (sessionId && user_id) {
        if (email && username) {
            // Remove login and register divs if user is logged in
            document.querySelectorAll('.one span').forEach(el => el.remove());
            document.querySelectorAll('.two p').forEach(el => el.remove());

            // Append the user's username and email to the DOM
            const usernameDiv = document.getElementById('username');
            const emailDiv = document.getElementById('email');

            if (usernameDiv) {
                usernameDiv.textContent = username;  // Update username in the DOM
            }
            if (emailDiv) {
                emailDiv.textContent = email;  // Update email in the DOM
            }
        }

        // Fetch events from the server using the session ID
        fetch(`http://localhost:5000/api/v1/user/${user_id}/events`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${sessionId}`  // Pass session ID if needed
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data && Array.isArray(data)) {
                    data.forEach(event => {
                        const eventHTML = `
                        <div class="evp" value="${event.id}">
                            <div class="eventbanner" name="banner">
                                <img src="${event.Banner}" alt="Event Banner">
                            </div>
                            <div class="eventattr">
                                <p class="eventstatus" name="status">${event.status}</p>
                                <p class="eventtitle" name="title">${event.title}</p>
                                <p class="eventdate" name="date">${event.Date}</p>
                                <p class="eventaddress" name="address">${event.Address}</p>
                                <p class="eventprice" name="price">${event.price}</p>
                            </div>
                        </div>`;
                        document.querySelector('.postscontainer').insertAdjacentHTML('beforeend', eventHTML);
                    });
                } else {
                    console.error('Invalid response format or missing events array.');
                }
            })
            .catch(error => {
                console.error('Error fetching events:', error);
            });
    } else {
        console.warn('No session ID found. Please login first.');
    }

    if (username) {
        const greetUserElement = document.querySelector('.greet-user p');
        const usernameElement = document.querySelector('.two p');
        if (greetUserElement) greetUserElement.textContent = 'Oh hello, ' + username + '!';
        if (usernameElement) usernameElement.textContent = username;
    }

    // Logout functionality
    const logoutButton = document.querySelector('.logout');
    if (logoutButton) {
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
                    credentials: 'include' // This includes cookies in the request
                })
                    .then(response => {
                        if (response.ok) {
                            // Clear local storage and redirect to login page
                            localStorage.clear();
                            window.location.href = 'login.html';
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
    }
});
