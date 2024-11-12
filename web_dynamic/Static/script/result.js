$(document).ready(function() {
  const eventContainer = $(".w-3\\/4"); // Escaped the / character

  // Function to fetch and render events based on search parameters
  async function fetchEvents() {
    try {
      // Get the search parameters from the URL
      const urlParams = new URLSearchParams(window.location.search);
      const params = urlParams.get('params');
      let searchParams = {};

      if (params) {
        // Parse the parameters from the URL
        searchParams = JSON.parse(decodeURIComponent(params));
      }

      // Send POST request with search parameters
      const response = await fetch('http://localhost:5000/api/v1/event_search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchParams), // Send the parameters in the request body
      });

      const events = await response.json();

      // Check if events were returned
      if (Array.isArray(events) && events.length > 0) {
        events.forEach(event => {
          const eventHTML = `
            <div class="w-full h-36 p-4 flex mb-4 cursor-pointer hover:drop-shadow-2xl hover:border-2 event-card" data-event-id="${event.id}">
                <!-- img div -->
                <div class="h-full w-4/12 pr-4">
                    <img src="${event.Banner}" alt="${event.title}" class="rounded h-full w-full object-fill" />
                </div>
                <!-- text-content -->
                <div class="h-full w-8/12 flex flex-col relative">
                    <h2 class="text-lg font-semibold">${event.title}</h2>
                    <p class="text-sm text-zinc-600 mt-1">${event.Date}</p>
                    <p class="text-sm mt-1 text-zinc-600">${event.Address}</p>
                    <p class="text-sm mt-2 font-semibold">From $${event.status}</p>
                    <div class="hidden hover:visible">
                        <div class="w-10 h-10 absolute right-40 bottom-0 flex items-center justify-center">
                            <i class="" title="Share" data-spec="icon" data-testid="icon">
                                <!-- Share icon here -->
                            </i>
                        </div>
                        <div class="w-10 h-10 absolute right-1/4 bottom-0 flex items-center justify-center">
                            <i class="eds-vector-image eds-icon--small eds-vector-image--grey-700 eds-vector-image--block" title="Like" data-spec="icon" data-testid="icon">
                                <!-- Heart icon here -->
                            </i>
                        </div>
                    </div>
                </div>
            </div>
          `;

          eventContainer.append(eventHTML); // Append the event card inside the container
        });

        // Add click event listeners to each event card
        $(".event-card").on("click", function() {
          const eventId = $(this).data("event-id");
          window.location.href = `eventspec.html?eventId=${eventId}`; // Redirect with event ID as a URL parameter
        });
      } else {
        console.error("No events found or an error occurred.");
      }
    } catch (error) {
      console.error("Error fetching events:", error);
    }
  }

  fetchEvents();
});
