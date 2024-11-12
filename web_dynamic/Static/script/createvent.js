document.addEventListener("DOMContentLoaded", function() {
    const sessionId = localStorage.getItem('session_id');
    const user_id = localStorage.getItem('user_id');

    if (sessionId) {

        function fetchLocations() {
            fetch('http://localhost:5000/api/v1/places', {
                method: 'GET'
            })
                .then(response => response.json())
                .then(data => {
                    const locationSelect = document.getElementById('eventloc');
                    data.forEach(function(location) {
                        const option = document.createElement('option');
                        option.value = location.id;
                        option.textContent = location.name;
                        locationSelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Error fetching locations:', error));
        }

        // Fetch and populate categories
        function fetchCategories() {
            fetch('http://localhost:5000/api/v1/catagory', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + sessionId
                }
            })
                .then(response => response.json())
                .then(data => {
                    const categorySelect = document.getElementById('eventcategory');
                    data.forEach(function(category) {
                        const option = document.createElement('option');
                        option.value = category.id;
                        option.textContent = category.name;
                        categorySelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Error fetching categories:', error));
        }

        fetchLocations();
        fetchCategories();

        // Format date to "YYYY-MM-DDTHH:MM:SS"
        // Format date to "YYYY-MM-DDTHH:MM:SS" without timezone info
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

        // Helper function to create a new place
        function createPlace(placedata) {
            return fetch('http://localhost:5000/api/v1/place', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + sessionId,
                    'Content-Type': 'application/json'
                },

                body: JSON.stringify(placedata)
            })
                .then(response => response.json())
                .catch(error => console.error('Error creating place:', error));
        }

        // Helper function to create a new category
        function createCategory(catagorydata) {
            return fetch('http://localhost:5000/api/v1/catagory', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + sessionId,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(catagorydata)
            })
                .then(response => response.json())
                .catch(error => console.error('Error creating category:', error));
        }

        // Event submission handling
        document.querySelector('.subb').addEventListener('click', async function(event) {
            event.preventDefault();



            let placeId = document.getElementById('eventloc').value;
            if (!placeId) {
                // Create a new place if not selected
                const placeName = document.getElementById('placename').value;
                const placeAddress = document.getElementById('placeaddress').value;
                const placePhone = document.getElementById('placephoneno').value
                const placedata = {
                    name : placeName,
                    address : placeAddress,
                    phone_number : placePhone

                };

                const newPlace = await createPlace(placedata);
                placeId = newPlace.id;
            }

            let categoryId = document.getElementById('eventcategory').value;
            if (!categoryId) {
                // Create a new category if not selected
                const categoryName = document.getElementById('catagoryname').value;
                const categoryDescription = document.getElementById('catagorydisc').value;
                const catagorydata = {
                    name : categoryName,
                    discription : categoryDescription
                };
                const newCategory = await createCategory(catagorydata);
                categoryId = newCategory.id;
            }

            const formData = {
                title: document.getElementById('eventtitle').value,
                description: document.getElementById('eventdescription').value,
                Date: formatDateToISO(document.getElementById('eventdate').value),
                place_id: placeId,
                status: "Active",
                catagories: [categoryId]
            };


            const fileInput = document.querySelector('.bannerr');
            const file = fileInput.files[0];

            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    formData.Banner = e.target.result;
                    submitEvent(formData);
                };
                reader.readAsDataURL(file);
            } else {
                submitEvent(formData);
            }
        });

        function submitEvent(formData) {
            fetch(`http://localhost:5000/api/v1/user/${user_id}/events`, {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + sessionId,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        return response.text().then(text => { throw new Error(text); });
                    }
                })
                .then(data => {
                    if (data && data.id) {
                        window.location.href = 'home.html';
                        alert('Event created successfully!');
                    } else {
                        alert('Failed to create event.');
                    }
                })
                .catch(error => {
                    console.error('Error creating event:', error);
                    alert('An error occurred while creating the event.');
                });
        }
    } else {
        window.location.href = 'login.html';
    }
});
