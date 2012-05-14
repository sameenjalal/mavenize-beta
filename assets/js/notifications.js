$(document).ready(function() {
  // Templates
  var notificationsTemplate = _.template("\
    <% for (var i = 0; i < notifications.length; i++) { %>\
      <% var notification = notifications[i]; %>\
        <li>\
          <a href='<%= notification.user_url %>'><%= notification.user_name %></a>\
          <%= notification.message %>\
          <% if (notification.item_name) { %>\
            <a href='<%= notification.item_url %>'><%= notification.item_name %></a>\
          <% } %>\
          .\
        </li>\
    <% } %>\
  ");

  // Initializers
  var badge = $("<span/>", { class: "badge badge-info", id: "notifications-count" });
  $.get('/notifications/count/', function(count) {
    badge.text(count | 0);
  })
  $('#notifications').append(badge);
  
  // SocketIO Listeners
  announce.on('notifications', function(data) {
    $('#notifications-count').text(data.new);
  });

  // jQuery Listeners
  $('#notifications').click(function() {
    if ($('#notifications-count').text() != "0" ||
        ! $('#notifications-dropdown ul').html().trim()) {
      $.get('/notifications/recent/', function(notifications) {
        var recent = notificationsTemplate({ notifications: notifications });
        $('#notifications-dropdown ul').empty()
        $('#notifications-dropdown ul').append(recent);
      });
    }
  });
});

// Initialize announce.js server
announce.init();
