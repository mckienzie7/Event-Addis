$(document).ready(function () {
    const url = 'http://0.0.0.0:5001/api/v1/status/';
    const urlevent = 'http://0.0.0.0:5001/api/v1/events';
    var eventdiv = $('.postcontainer');

    $.get(url, function (data) {
        if (data.status === 'OK') {
            $.get(urlevent, function (events) {
                eventdiv.append(events.map(event => {
                    return `<div class="evp">
                                <div class="eventbanner" name="banner">
                                    <img src="../dumb/How%20to%20spend%20a%20perfect%20day%20in%20Addis%20Ababa.jpeg" alt="">
                                </div>
                                <div class="eventattr">
                                    <p class="eventstatus" name="status">${event.status}</p>
                                    <p class="eventtitle" name="title">${event.title}</p>
                                    <p class="eventdate" name="date">${event.date}</p>
                                    <p class="eventaddress" name="address">${event.address}</p>
                                    <p class="eventprice" name="price">Free</p>
                                </div>
                            </div>`;
                })).join(''));
            });
        } else {
            $('div#api_status').removeClass('available');
        }
    });
});
