$(document).ready(function() {


    var accessToken = localStorage.getItem('accessToken');

    if(accessToken){
        
    }
    $.ajax({
        url: 'http://localhost:5000/api/v1/event',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            if (response && Array.isArray(response)) {
                response.forEach(function(event) {
                    var eventHTML = '<div class="evp" value="'+ event.id +'">' +
                        '<div class="eventbanner" name="banner">' +
                        '<img src="' + event.Banner + '" alt="">' +
                        '</div>' +
                        '<div class="eventattr">' +
                        '<p class="eventstatus" name="status">' + event.status + '</p>' +
                        '<p class="eventtitle" name="title">' + event.title + '</p>' +
                        '<p class="eventdate" name="date">' + event.Date + '</p>' +
                        '<p class="eventaddress" name="address">' + event.Address + '</p>' +
                        '<p class="eventprice" name="price">' + event.price + '</p>' +
                        '</div>' +
                        '</div>';

                    $('.eventposts .postscontainer').append(eventHTML);
                });
            } else {
                console.error('Invalid response format or missing events array.');
            }
        },
        error: function(xhr, status, error) {
            console.error('Error fetching events:', error);
        }
    });
});
