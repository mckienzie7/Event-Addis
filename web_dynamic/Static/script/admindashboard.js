document.addEventListener("DOMContentLoaded", function () {
    // Immediately check for session and admin privileges
    const sessionId = localStorage.getItem('session_id');
    const admin = localStorage.getItem('admin');

    if (!sessionId || admin !== 'true') {
        window.location.href = 'login.html';
        return;
    }

    function fetchEvents() {
        fetch('http://localhost:5000/api/v1/event', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${sessionId}`
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch events');
            }
            return response.json();
        })
        .then(data => {
            if (Array.isArray(data)) {
                document.querySelector('.llmid .content').innerHTML = ''; // Clear existing events
                data.forEach(event => {
                    const eventHTML = `
                        <div class="content" id="page">
                            <p>${event.id}</p>
                            <div><img src="${event.Banner}" alt="Event Banner"></div>
                            <p>${event.title}</p>
                            <p>${event.organizer}</p>
                            <p>${event.Date}</p>
                            <p>${event.status}</p>
                            <div>
                                <a href="#" onclick="deleteEvent(${event.id}); return false;">
                                    <i class="fa-solid fa-square-xmark" id="x"></i>
                                </a>
                            </div>
                        </div>`;
                    document.querySelector('.llmid').insertAdjacentHTML('beforeend', eventHTML);
                });
            } else {
                console.error('Invalid event data format');
            }
        })
        .catch(error => {
            console.error('Error fetching events:', error);
        });
    }

    // Function to delete an event
    function deleteEvent(eventId) {
        if (confirm('Are you sure you want to delete this event?')) {
            fetch(`http://localhost:5000/api/v1/events/${eventId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${sessionId}`
                }
            })
            .then(response => {
                if (response.ok) {
                    console.log('Event deleted successfully');
                    fetchEvents(); // Reload events
                } else {
                    throw new Error('Failed to delete event');
                }
            })
            .catch(error => {
                console.error('Error deleting event:', error);
            });
        }
    }

    // Fetch events on page load
    fetchEvents();
});
