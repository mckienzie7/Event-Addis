$(document).ready(function() {
    // Function to retrieve session ID and email from localStorage
    const sessionId = localStorage.getItem('session_id');
    const email = localStorage.getItem('email');

    // Category-to-icon dictionary
    const categoryIcons = {
        "Music": "fa-solid fa-music",
        "Nightlife": "fa-solid fa-martini-glass-citrus",
        "Holiday": "fa-regular fa-calendar-days",
        "Art": "fa-solid fa-masks-theater",
        "Food&Drinks": "fa-solid fa-utensils",
        "Hiking": "fa-solid fa-mountain"
    };

    // If there's a session ID, proceed with the logic
    if (sessionId) {
        // Modify DOM if user is logged in
        if (email) {
            $('.topr .regh').remove();
            $('.topr .loginh').html(`<span>${email}</span>`);
        }

        // Fetch event data from the server using the session ID
        fetch('http://localhost:5000/api/v1/event', {
            method: 'GET',
        })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                if (data && Array.isArray(data)) {
                    data.forEach(event => {
                        // Use category name to find the icon from the dictionary
                        const categoryIconClass = categoryIcons[event.category] || "fa-solid fa-question";

                        const eventHTML = `
                        <div class="evp" data-event-id="${event.id}">
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

                        // Append the event HTML to the container
                        $('.eventposts .postscontainer').append(eventHTML);
                    });

                    // Add click event listener for each event div
                    $('.evp').on('click', function() {
                        const eventId = $(this).data('event-id');
                        // Redirect to eventspec.html with event ID as URL parameter
                        window.location.href = `eventspec.html?eventId=${eventId}`;
                    });
                } else {
                    console.error('Invalid response format or missing events array.');
                }
            })
            .catch(error => {
                console.error('Error fetching events:', error);
            });

        // Fetch categories from the server (to populate category list)
        fetch('http://localhost:5000/api/v1/catagory', {
            method: 'GET',
        })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(categories => {
                if (categories && Array.isArray(categories)) {
                    categories.forEach(category => {
                        const categoryIconClass = categoryIcons[category.name] || "fa-solid fa-question";
                        const categoryHTML = `
                        <div class="catt" id="catt-${category.name}" data-category-id="${category.id}">
                            <div class="cat1">
                                <i class="${categoryIconClass}"></i>
                            </div>
                            <p class="category-name">${category.name}</p>
                        </div>`;
                        $('.category-container').append(categoryHTML);
                    });
                } else {
                    console.error('Invalid response format or missing categories array.');
                }
            })
            .catch(error => {
                console.error('Error fetching categories:', error);
            });
    }
});
