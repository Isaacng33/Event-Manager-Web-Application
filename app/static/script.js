// Automatically hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        var flashMessage = document.getElementById('flash-message');
        if (flashMessage) {
            flashMessage.style.opacity = '0';
            setTimeout(function() {
                flashMessage.remove();
            }, 500);
        }
    }, 3000); // Adjust the time (in milliseconds) as needed
});

$(document).ready(function () {
  // Add a click event listener to all elements with the class 'like-button'
  $('.like-button').on('click', function (event) {

    // Access the data-event-id attribute of the clicked button
    var eventId = $(this).data('event-id');
    var likeCountElement = $(this).closest('.card-body').find('.like-count');
    var likeButton = $(this).closest('.card-body').find('.like-button');

    // AJAX request to update the web
    $.ajax({
      url: '/like_event',
      method: 'POST',
      data: { event_id: eventId },
      success: function (response) {
        // update UI
        likeCountElement.text(response.likes);
        if (response.success) {
          likeButton.html('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#E6E6FA" class="bi bi-heart-fill" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/></svg>');
        } else {
          likeButton.html('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#E6E6FA" class="bi bi-heart" viewBox="0 0 16 16"><path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/></svg>');
        }
      },
    });
  });
});

$(document).ready(function() {
  // Add click event listener to the button
  $('#filterButton').click(function() {
      // Toggle the display of the form
      $('#filterForm').toggle();
  });
});

$(document).ready(function() {
  // Add click event listener to the button
  $('#clearFilter').click(function() {
      // Toggle the display of the form
      $('#filterForm').trigger('reset');
  });
});

$(document).ready(function () {
  // Initialize Cookie Consent
  window.cookieconsent.initialise({
      "palette": {
          "popup": { "background": "#292929" }
      },
      "content": {
          "message": "This website uses cookies to ensure you get the best experience on our website.",
          "dismiss": "Got it!",
          "link": "Learn more",
          href: "/cookie-policy"
      },
      "elements": {
        "button": "<a aria-label='cookie-consent' tabindex='0' class='cc-btn cc-dismiss btn'>Got it!</a>"
    },
  });
});