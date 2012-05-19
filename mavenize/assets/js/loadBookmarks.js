(function($) {
  // Templates
  var bookmarkTemplate = _.template("\
    <% for (var i = 0; i < movies.length; i++) { %>\
      <% var movie = movies[i]; %>\
      <li class='span2' data-next='<% movie.next %>'>\
        <a class='thumbnail bookmark' data-item='<%= movie.item_id %>'>\
          <img src='<%= movie.image_url %>' />\
          <% if (movie.new_bookmarks >= 1) { %>\
            <span class='badge badge-info bookmarks-count'><%= movie.new_bookmarks %></span>\
          <% } %>\
        </a>\
      </li>\
    <% } %>\
  ");

  // Plugins
  $.fn.loadBookmarks = function(url) {
    listSelector = $(this);
    $.get(url, function(movies) {
      var thumbnails = bookmarkTemplate({ movies: movies });
      $(listSelector).append(thumbnails);
      $(listSelector).trigger('appended');
    });
  }
}) (jQuery);


(function($) {
  // Templates
  var userTemplate = _.template("\
    <% if (friends.length == 0) { %>\
      <tr><td>No one has marked this yet.</td></tr>\
    <% } %>\
    <% for (var i = 0; i < friends.length; i++) { %>\
      <% var friend = friends[i]; %>\
      <tr>\
        <td class='bookmark-thumbnail'><a href='<%= friend.user_url %>'><img src='<%= friend.user_thumbnail %>' /></a></td>\
        <td><a href='<%= friend.user_url %>'><%= friend.user_name %></a></td>\
      </tr>\
    <% } %>\
  ");
 
  $.fn.loadFriendBookmarks = function(url) {
    listSelector = $(this);
    $.get(url, function(friends) {
      var users = userTemplate({ friends: friends });
      $(listSelector).append(users);
    });
  }
}) (jQuery);

