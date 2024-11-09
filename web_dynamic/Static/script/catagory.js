document.addEventListener('DOMContentLoaded', function() {
    // Get the category ID from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const categoryId = urlParams.get('category_id');  // Get the category_id from URL
    
    if (categoryId) {
        // Fetch the specific category from the backend
        fetch(`http://localhost:5000/api/v1/catagory/${categoryId}`, {
            method: 'GET',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(category => {
            if (category) {
                // Insert category data into the page
                const categoryHTML = `
                    <div class="description-part">
                        <div>
                            <p class="p-catagory-event">${category.name} events</p>
                            <p class="p11">In Addis Ababa, Ethiopia</p>
                            <p class="pdisc">Discover ${category.discription} events in your area and online</p>
                        </div>
                    </div>
                    <div class="photo-part">
                        <div class="immg">
                            <img src="${category.image || 'default-image.jpg'}" alt="${category.name} category image">
                        </div>
                    </div>
                `;

                // Add the HTML to the page (e.g., inside `.cover-part`)
                document.querySelector('.cover-part').innerHTML = categoryHTML;
                
                // Optionally, fetch the events related to this category and display them
                fetchEventsForCategory(categoryId);
            } else {
                console.error('Category not found.');
            }
        })
        .catch(error => {
            console.error('Error fetching category:', error);
        });
    } else {
        console.error('No category ID in the URL.');
    }

    // Function to fetch events for a specific category
    function fetchEventsForCategory(categoryId) {
        fetch(`http://localhost:5000/api/v1/${categoryId}/events`, {
            method: 'GET',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(events => {
            if (events && Array.isArray(events)) {
                events.forEach(event => {
                    const eventHTML = `
                        <div class="evp">
                            <div class="eventbanner" name="banner">
                                <img src="${event.Banner}" alt="Event banner">
                            </div>
                            <div class="eventattr">
                                <p class="eventstatus" name="status">${event.status}</p>
                                <p class="eventtitle" name="title">${event.title}</p>
                                <p class="eventdate" name="date">${event.Date}</p>
                                <p class="eventaddress" name="address">${event.Address}</p>
                                <p class="eventprice" name="price">${event.price}</p>
                            </div>
                        </div>
                    `;
                    // Append the event to the container
                    document.querySelector('.eventposts .postscontainer').insertAdjacentHTML('beforeend', eventHTML);
                });
            } else {
                console.error('No events found for this category.');
            }
        })
        .catch(error => {
            console.error('Error fetching events:', error);
        });
    }
});