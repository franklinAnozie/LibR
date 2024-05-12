/* eslint-disable no-undef */
$(document).ready(function () {
  const apiUrl = 'http://localhost:5000/api/v1/books/';

  $.getJSON(apiUrl, function (data) {
    const books = data;

    books.forEach(function (book) {
      const title = book.title;
      const author = book.author;
      const bookId = book.id;
      //const coverId = book.work.cover_id;
      //const coverUrl = 'https://covers.openlibrary.org/b/id/' + coverId + '-L.jpg'; // Construct cover image URL

      // Create HTML elements for each book and append to #books div
      let bookHtml = '<div>';
      bookHtml += '<img src="../static/images/book.gif" alt="' + title + '">';
      bookHtml += '<p>Author: ' + author + '</p>';
      bookHtml += '<button class="borrow borrow-btn" data-book-id="' + bookId + '">Borrow</button>';
      bookHtml += '</div>';

      $('#books').append(bookHtml);
    });

    $('.borrow').click(function () {
      const bookId = $(this).data('book-id');
      console.log(bookId);

      // Fetch user ID from Flask endpoint
      fetch('/get_user_id')
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch user ID');
          }
          return response.json();
        })
        .then(data => {
          var userId = data.user_id;
          console.log(userId);

          // Make AJAX request to borrow the book
          $.ajax({
            url: 'http://localhost:5000/api/v1/books/' + bookId + '/borrow/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ user_id: userId }),
            success: function (response) {
              alert(response.message);
              // You can perform additional actions after successfully borrowing the book
            },
            error: function (xhr, status, error) {
              alert('Error: ' + xhr.responseText + " " + status + " " + error);
            }
          });
        })
        .catch(error => {
          console.error('Error fetching user ID:', error);
          alert('Error fetching user ID: ' + error.message);
        });
    });

    $('.dropMenu').click(function () {
      $(this).find('.Menu').toggle();
    });

    $('#signup-btn').click(function (event) {
      // Prevent the default form submission
      event.preventDefault();

      // Get form data
      var first = $('#first').val();
      var last = $('#last').val();
      var email = $('#email').val();
      var username = $('#username').val();
      var password = $('#password').val();

      var formData = {
        first: first,
        last: last,
        email: email,
        username: username,
        password: password
      };
      console.log(formData);
      // Send POST request to Flask route
      $.ajax({
        url: '/signup',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function (response) {
          // Handle success response from Flask
          console.log('Signup successful');
          alert('Signup successful');
          // Optionally, redirect to another page
          window.location.href = '/login'; // Redirect to login page after signup
        },
        error: function (xhr, status, error) {
          // Handle error response from Flask
          alert('Error: ' + xhr.responseText + " " + status + " " + error);
        }
      });
    });
  });
});