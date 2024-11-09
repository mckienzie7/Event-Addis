document.addEventListener("DOMContentLoaded", function() {
    // Function to get a cookie value by name
    function getCookie(name) {
        let match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? match[2] : null;
    }

    const sessionId = localStorage.getItem('session_id'); 
    const user_id = localStorage.getItem('user_id');

    if (sessionId) {
        // Function to fetch locations from Flask endpoint
        function fetchLocations() {
            fetch('http://localhost:5000/api/v1/places', {
                method: 'GET',
            })
            .then(response => response.json())
            .then(data => {
                // Loop through the response data and populate the location dropdown
                data.forEach(function(location) {
                    document.querySelector('.endinp').innerHTML += `<option value="${location.id}">${location.name}</option>`;
                });
            })
            .catch(error => console.error('Error fetching locations:', error));
        }

        // Function to fetch categories from Flask endpoint
        function fetchCategories() {
            fetch('http://localhost:5000/api/v1/catagory', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + sessionId
                }
            })
            .then(response => response.json())
            .then(data => {
                // Loop through the response data and populate the category dropdown
                data.forEach(function(category) {
                    document.querySelector('#eventcategory').innerHTML += `<option value="${category.id}">${category.name}</option>`;
                });
            })
            .catch(error => console.error('Error fetching categories:', error));
        }

        // Call fetchLocations and fetchCategories functions when the page is loaded
        fetchLocations();
        fetchCategories();

        // Event listener for form submission
        document.querySelector('.subb').addEventListener('click', function(event) {
            event.preventDefault();
        
            // Gather form data
            var formData = {
                title: document.getElementById('eventtitle').value,
                discription: document.getElementById('eventdescription').value,
                Date: formatDateToISO(document.getElementById('eventdate').value),
                place_id: document.getElementById('eventloc').value,
                Banner: "",
                categories: null  // Store a single category ID
            };

            // Collect selected category
            const selectedCategory = document.getElementById('eventcategory').value;
            if (selectedCategory) {
                formData.category_id = selectedCategory;  // Only one category selected
            }

            const fileInput = document.querySelector('.bannerr');
            const file = fileInput.files[0];
            
            if (file) {
                // Only create event once the image is fully read
                var reader = new FileReader();
                reader.onload = function(e) {
                    formData.Banner = e.target.result; // base64 encoded image
                    if (!formData.place_id) {
                        createNewLocationAndEvent(formData);
                    } else {
                        createEvent(formData);
                    }
                };
                reader.readAsDataURL(file); // Read the file as a data URL
            } else {
                // If no image is provided, continue without setting Banner
                if (!formData.place_id) {
                    createNewLocationAndEvent(formData);
                } else {
                    createEvent(formData);
                }
            }
        });
        
        // Function to format the date in YYYY-MM-DDTHH:MM:SS format
        function formatDateToISO(dateString) {
            const date = new Date(dateString);
            const year = date.getFullYear();
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const day = date.getDate().toString().padStart(2, '0');
            const hours = date.getHours().toString().padStart(2, '0');
            const minutes = date.getMinutes().toString().padStart(2, '0');
            const seconds = date.getSeconds().toString().padStart(2, '0');
            
            return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
        }

        // Function to create a new location and then the event
        function createNewLocationAndEvent(formData) {
            const new_place = {
                name: document.getElementById('placename').value,
                address: document.getElementById('placeaddress').value,
                phone_number: document.getElementById('placephoneno').value
            };
        
            fetch('http://localhost:5000/api/v1/place', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + sessionId,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(new_place)
            })
            .then(response => response.json())
            .then(location => {
                formData.place_id = location.id;
                createEvent(formData); // Now create the event with the new place ID
            })
            .catch(error => console.error('Error creating location:', error));
        }
        
        // Function to create the event
        function createEvent(formData) {
            fetch(`http://localhost:5000/api/v1/user/${user_id}/events`, {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + sessionId,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data && data.id) {
                    window.location.href = 'home.html';
                    console.log('Event created successfully:', data);
                }
            })
            .catch(error => console.error('Error creating event:', error));
        }        
    } else {
        // If no valid session, redirect to login page
        window.location.href = 'login.html';
    }
});
