document.addEventListener('DOMContentLoaded', function() {
    // Function to retrieve session ID from localStorage
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

        // Fetch data from the server using the session ID
        fetch(`http://localhost:5000/api/v1/user/${user_id}/events`, {
            method: 'GET',
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
                                <img src="${event.Banner}" alt="">
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
});
