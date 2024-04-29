/* eslint-disable no-undef */
$(document).ready(function () {
  const apiUrl = 'https://openlibrary.org/people/mekBot/books/want-to-read.json';

  $.getJSON(apiUrl, function (data) {
    const books = data.reading_log_entries;

    books.forEach(function (book) {
      const title = book.work.title;
      const author = book.work.author_names.join(', '); // If there are multiple authors
      const coverId = book.work.cover_id;
      const coverUrl = 'https://covers.openlibrary.org/b/id/' + coverId + '-L.jpg'; // Construct cover image URL

      // Create HTML elements for each book and append to #books div
      let bookHtml = '<div>';
      bookHtml += '<h2>' + title + '</h2>';
      bookHtml += '<img src="' + coverUrl + '" alt="' + title + '">';
      bookHtml += '<p>Author: ' + author + '</p>';
      bookHtml += '</div>';

      $('#books').append(bookHtml);
    });
  });
});
