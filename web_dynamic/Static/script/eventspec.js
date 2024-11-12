document.addEventListener('DOMContentLoaded', function() {
    // Get the event ID from the URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const eventId = urlParams.get('eventId');

    if (eventId) {
        // Fetch the event data from the server
        fetch(`http://localhost:5000/api/v1/event/${eventId}`, {
            method: 'GET',
        })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(event => {
                // Check if event data is available and render the HTML structure
                if (event) {
                    const eventHTML = `
                    <div class="bg-white rounded-lg overflow-hidden shadow-md">
                        <div class="relative">
                            <!-- Event Image -->
                            <img src="${event.Banner || 'default-banner.jpg'}" alt="${event.title}" class="w-full h-64 object-cover">
                        </div>
                        <div class="p-6">
                            <h2 class="text-2xl font-bold text-gray-800">${event.title}</h2>
                            <p class="text-gray-600 mt-2">${event.description || 'Description unavailable'}</p>
                            <p class="mt-4 text-lg font-semibold text-gray-700">${event.Date}</p>
                            <p class="text-gray-500">${event.Time}</p>
                            <p class="text-gray-500">${event.Address}</p>

                            <!-- Ticket Button -->
                            <button id="ticketButton" class="mt-6 bg-purple-500 text-white px-4 py-2 rounded-md">
                                ${event.status === 'Active' ? 'Get Tickets' : 'Ticket sales ended'}
                            </button>
                        </div>
                    </div>
                `;

                    // Insert the generated HTML into the main content area
                    document.querySelector('main').innerHTML = eventHTML;

                    // Add event listener to the ticket button
                    const ticketButton = document.getElementById('ticketButton');
                    if (ticketButton) {
                        ticketButton.addEventListener('click', () => {
                            if (event.status === 'Active') {
                                showModal();
                            } else {
                                alert("Ticket sales have ended.");
                            }
                        });
                    }
                } else {
                    console.error('Event not found.');
                }
            })
            .catch(error => {
                console.error('Error fetching event data:', error);
            });
    }

    // Modal display functions
    const modal = document.getElementById('ticketModal');
    const closeModal = document.getElementById('closeModal');
    const confirmBooking = document.getElementById('confirmBooking');

    function showModal() {
        modal.classList.remove('hidden');
    }

    function hideModal() {
        modal.classList.add('hidden');
    }

    // Hide the modal on close button click
    closeModal.addEventListener('click', hideModal);

    // Confirm booking button logic
    confirmBooking.addEventListener('click', () => {
        const ticketType = document.querySelector('input[name="ticketType"]:checked');
        if (ticketType) {
            alert(`You have booked a ${ticketType.value} ticket!`);
            hideModal();
        } else {
            alert('Please select a ticket type.');
        }
    });
});
