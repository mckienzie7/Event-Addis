document.addEventListener('DOMContentLoaded', function() {
    // Function to handle redirection when the arrow button is clicked
    function redirectToResults() {
        // Get the values from the input fields
        const eventName = document.querySelector('.event-title-search-inp').value;
        const eventLocation = document.querySelector('.event-title-location-inp').value;

        // Create a JSON object for the parameters
        let searchParams = {};

        // Add name and location to the object if they are not empty
        if (eventName) {
            searchParams.title = eventName;
        }

        if (eventLocation) {
            searchParams.Address = eventLocation;
        }

        // If either name or location is provided, redirect
        if (Object.keys(searchParams).length > 0) {
            // Encode the search parameters as a JSON string
            const jsonParams = encodeURIComponent(JSON.stringify(searchParams));

            // Redirect to result.html with JSON parameters in the URL
            window.location.href = `../templates/result.html`;
        }
    }

    // Attach the redirectToResults function to the arrow button click event
    const arrowButton = document.querySelector('#ar');
    if (arrowButton) {
        arrowButton.addEventListener('click', redirectToResults);
    }
});
