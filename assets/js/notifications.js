$(document).ready(function() {
  // Templates
  var miniNotificationTemplate = _.template("\
    <% for (var i = 0; i < notifications.length; i++) { %>\
      <% var notification = notifications[i]; %>\
        <li>\
          <div class='user-mini-thumbnail pull-left'>\
            <a href='<%= notification.user_url %>'>\
              <img src='<%= notification.user_avatar %>' />\
            </a>\
          </div>\
          <a href='<%= notification.user_url %>'><%= notification.user_name %></a>\
          <%= notification.message %>\
          <% if (notification.item_name) { %>\
            <a href='<%= notification.item_url %>'><%= notification.item_name %></a>.\
          <% } %>\
          <div class='mini-timestamp pull-right'>\
            <%= notification.time_since %> ago\
          </div>\
          <div style='clear: both;'></div>\
        </li>\
        <li class='divider'></li>\
    <% } %>\
    <li id='all-notifications'>\
      <a href='/me/#notifications'>See All Notifications</a>\
    </li>\
  ");

  // Initializers
  var badge = $("<span/>", { class: "badge badge-info", id: "notifications-count" });
  $.get('/notifications/count/', function(count) {
    badge.text(count | 0);
  })
  $('#notifications-link').append(badge);

  if (window.location.hash == "#notifications") {
    $('#filters li').removeClass('active');
    $('#filters a[href="#notifications"]').tab('show').addClass('active');
  }
    
  
  // SocketIO Listeners
  announce.on('notifications', function(data) {
    $('#notifications-count').text(data.new);
  });

  // jQuery Listeners
  $('#notifications-link').click(function() {
    if ($('#notifications-count').text() != "0" ||
        ! $('#notifications-dropdown ul').html().trim()) {
      $.get('/notifications/recent/', function(notifications) {
        var recent = miniNotificationTemplate({ notifications: notifications });
        $('#notifications-dropdown ul').empty()
        $('#notifications-dropdown ul').append(recent);
      });
    }
    $('#notifications-count').text("0");
  });
});

// Initialize announce.js server
announce.init();
