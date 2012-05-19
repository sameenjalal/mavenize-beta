$(document).ready(function() {
  // Templates
  var modalTemplate = _.template("\
    <div class='modal-header'>\
      <a class='close' data-dismiss='modal'>×</a>\
      <h3>The Latest on Your Bookmarks</h3>\
    </div>\
    <div class='modal-body'>\
      <div class='container bookmark-container'>\
        <div class='row'>\
          <div class='span8'>\
            <ul class='thumbnails'></ul>\
            <div class='paginator'></div>\
          </div>\
          <div class='span3'>\
            <h3>Your Friends</h3>\
            <table class='table bookmarks-table'>\
              <tbody>\
              <td>Select a movie from the left to see who wants to go.</td>\
              </tbody>\
            </table>\
          </div>\
        </div>\
      </div>\
    </div>\
  ");

 
  // Helper Functions
  var getBookmarksUrl = function(page) {
    return '/bookmarks/' + page + '/'; 
  }

  var getFriendBookmarksUrl = function(itemId) {
    return '/bookmarks/item/' + itemId + '/'
  }

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
    var skeleton = modalTemplate();
    $('#bookmarks').append(skeleton);
    $('#bookmarks').trigger('skeleton');
  });

  $('#bookmarks').bind('skeleton', function() {
    $('#bookmarks .thumbnails').loadBookmarks( getBookmarksUrl(1) );
  });

  $('#bookmarks').bind('appended', function() {
    var nextPage = $('.bookmark:last').attr('data-next');
    $('#bookmarks .thumbnails a').each(function() {
      $(this).bind('click', function() {
        $(this).find('span').remove();
        $('#bookmarks .bookmarks-table tbody').empty();
        $('#bookmarks .bookmarks-table tbody').loadFriendBookmarks(
          getFriendBookmarksUrl($(this).attr('data-item'))
        );
      });
    });
  });
});
