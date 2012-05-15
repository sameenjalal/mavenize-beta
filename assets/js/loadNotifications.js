(function($) {
  // Templates
  var notificationTemplate = _.template("\
    <% for (var i = 0; i < notifications.length; i++) { %>\
      <% var notification = notifications[i]; %>\
        <li class='notification' data-next='<%= notification.next %>'>\
          <div class='user-thumbnail pull-left'>\
            <a href='<%= notification.user_url %>'>\
              <img src='<%= notification.user_avatar %>' />\
            </a>\
          </div>\
          <div class='notification-meta'>\
            <a href='<%= notification.user_url %>'><%= notification.user_name %></a>\
            <%= notification.message %>\
            <% if (notification.item_name) { %>\
              <a href='<%= notification.item_url %>'><%= notification.item_name %></a>.\
            </div>\
          <% if (notification.thank_you) { %>\
            <div class='notification-text'>\
              <%= notification.thank_you %>\
            </div>\
          <% } %>\
          <% } %>\
          <div class='timestamp pull-right'>\
            <%= notification.time_since %> ago\
          </div>\
          <div style='clear: both;'></div>\
        </li>\
    <% } %>\
  ");

  $.fn.loadNotifications = function(url) {
    listSelector = $(this);
    $.get(url, function(notifications) {
      var list = notificationTemplate({ notifications: notifications });
      listSelector.append(list);
      listSelector.trigger('appended');
    });
  }

}) (jQuery);
