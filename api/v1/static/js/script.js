/* eslint-disable no-undef */
$(document).ready(function () {
  const apiUrl = '/api/v1/books/';

  $.getJSON(apiUrl, function (data) {
    const books = data;

    books.forEach(function (book) {
      const title = book.title;
      const author = book.author;
      const bookId = book.id;
      // const coverId = book.work.cover_id;
      // const coverUrl = 'https://covers.openlibrary.org/b/id/' + coverId + '-L.jpg'; // Construct cover image URL

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

      // Fetch user ID from Flask endpoint
      fetch('/app/get_user_id')
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch user ID');
          }
          return response.json();
        })
        .then(data => {
          const userId = data.user_id;

          // Make AJAX request to borrow the book
          $.ajax({
            url: '/api/v1/books/' + bookId + '/borrow/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ user_id: userId }),
            success: function (response) {
              alert(response.message);
              // You can perform additional actions after successfully borrowing the book
            },
            error: function (xhr, status, error) {
              alert(`Error: ${xhr.responseText} ${status} ${error}`);
            }
          });
        })
        .catch(error => {
          alert('Error fetching user ID: ' + error.message);
        });
    });

    // login
    $('#login-btn').click(function (event) {
    // Get username and password from input fields
      event.preventDefault();
      const username = $('#username').val();
      const password = $('#password').val();

      // Send POST request to Flask route
      $.ajax({
        url: '/app/login-post',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ username, password }),
        success: function (response) {
          // Handle success response from Flask
          alert('You Logged in !');
          // Optionally, redirect to another page
          window.location.href = '/app/';
        },
        error: function (xhr, status, error) {
          alert(`Error: ${xhr.responseText} ${status} ${error}`);
        }
      });
    });

    $('.dropMenu').click(function () {
      $(this).find('.Menu').toggle();
    });

    $('#signup-btn').click(function (event) {
      // Prevent the default form submission
      event.preventDefault();

      // Get form data
      const first = $('#first').val();
      const last = $('#last').val();
      const email = $('#email').val();
      const username = $('#username').val();
      const password = $('#password').val();

      const formData = {
        first,
        last,
        email,
        username,
        password
      };
      // Send POST request to Flask route
      $.ajax({
        url: '/app/signup',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function (response) {
          // Handle success response from Flask
          alert('Signup successful');
          // Optionally, redirect to another page
          window.location.href = '/app/login'; // Redirect to login page after signup
        },
        error: function (xhr, status, error) {
          // Handle error response from Flask
          alert(`Error: ${xhr.responseText} ${status} ${error}`);
        }
      });
    });
  });
});
