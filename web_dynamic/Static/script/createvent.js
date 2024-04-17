$(document).ready(function() {
    var accessToken = localStorage.getItem('accessToken');
    var role = localStorage.getItem('Role');
    var user_info = JSON.parse(localStorage.getItem('user_info'));

    // Check if the user is an organizer or administrator
    if (accessToken && (role === 'organizer' || role === 'administrator')) {
        // Function to fetch locations from Flask endpoint
        function fetchLocations() {
            $.ajax({
                url: 'http://localhost:5000/api/v1/places',
                type: 'GET',
                success: function (response) {
                    // Loop through the response data and populate the select element
                    response.forEach(function (location) {
                        $('.endinp').append('<option value="' + location.id + '">' + location.name + '</option>');
                    });
                },
                error: function (xhr, status, error) {
                    console.error('Error fetching locations:', error);
                    // Optionally, display an error message to the user
                }
            });
        }

        function fetchcatagories() {
            $.ajax({
                url: 'http://localhost:5000/api/v1/catagory',
                type: 'GET',
                success: function (response) {
                    // Loop through the response data and populate the select element
                    response.forEach(function (catagory) {
                        $('.catagory-list').append('<div class="catagory" value="' + catagory.id+'">' + catagory.name + '</div>');
                    });
                },
                error: function (xhr, status, error) {
                    console.error('Error fetching locations:', error);
                    // Optionally, display an error message to the user
                }
            });
        }

        // Call fetchLocations function when the page is loaded
        fetchLocations();
        fetchcatagories();

        // Event listener for form submission
        $('.subb').click(function (event) {
            event.preventDefault();

            const user_id = user_info.user_id;

            var formData = {
                title: $('#eventtitle').val(),
                discription: $('#eventdescription').val(),
                Date: $('#eventdate').val(),
                place_id : $('#eventloc option:selected').attr('value'),
                Banner : "",
                user_id: user_id
            };

            var fileInput = $('.bannerr')[0];
            var file = fileInput.files[0];
            if (file) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    formData.Banner = e.target.result; // Set banner as base64 encoded string
                };
                reader.readAsDataURL(file); // Read file as data URL
            }

            // If there is no Location chosen from the option
            if (!formData.place_id ){
                const placename = $('#placename').val();
                const placeaddress = $('#placeaddress').val();
                const placephone = $('#placephoneno').val();
                const new_place = {
                    name : placename,
                    address : placeaddress,
                    phone_number : placephone
                };

                // AJAX call to create a new place
                $.ajax({
                    url: 'http://localhost:5000/api/v1/place' ,
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(new_place),
                    success: function (location) {
                        formData.place_id = location.id;

                        // AJAX call to create a new event
                        createEvent(formData, user_id);
                    },
                    error: function (xhr, status, error) {
                        // Handle error response
                        console.error('Error creating Location:', error);
                        // Optionally, display an error message to the user
                    }
                });
            } else {
                // If location is chosen, directly create the event
                createEvent(formData, user_id);
            }
        });
    }
    else{
        window.location.href = 'login.html';
    }
});

function createEvent(formData, user_id) {
    $.ajax({
        url: 'http://localhost:5000/api/v1/user/'+user_id+'/event',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function (response) {
            // Handle success response
            console.log('Event created successfully:', response);
            console.log(response);

            // Optionally, redirect to another page or show a success message
        },
        error: function (xhr, status, error) {
            // Handle error response
            console.error('Error creating event:', error);
            // Optionally, display an error message to the user
        }
    });
}
