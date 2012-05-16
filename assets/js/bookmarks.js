$(document).ready(function() {
  // Initializers
  var badge = $('<span/>', { class: 'badge badge-info', id: 'bookmarks-count'});
  $.get('/bookmarks/count/', function(count) {
    badge.text(count | 0);
  });
  $('#bookmarks-link').append(badge);

  // SocketIO Listeners
  announce.on('bookmark', function(data) {
    var currentCount = parseInt($('#bookmarks-count').text());
    $('#bookmarks-count').text(++currentCount);
  });

  // jQuery Listeners
  $('#bookmarks-link').click(function() {
    $('#bookmarks-count').text("0");
  });
});
