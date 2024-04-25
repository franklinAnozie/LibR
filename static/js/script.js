$(document).ready(function() {
    var apiUrl = 'https://openlibrary.org/people/mekBot/books/want-to-read.json';

    $.getJSON(apiUrl, function(data) {
        var books = data.reading_log_entries;

        books.forEach(function(book) {
            var title = book.work.title;
            var author = book.work.author_names.join(', '); // If there are multiple authors
            var coverId = book.work.cover_id;
            var coverUrl = 'https://covers.openlibrary.org/b/id/' + coverId + '-L.jpg'; // Construct cover image URL

            // Create HTML elements for each book and append to #books div
            var bookHtml = '<div>';
            bookHtml += '<h2>' + title + '</h2>';
            bookHtml += '<img src="' + coverUrl + '" alt="' + title + '">';
            bookHtml += '<p>Author: ' + author + '</p>';
            bookHtml += '</div>';

            $('#books').append(bookHtml);
        });
    });
});