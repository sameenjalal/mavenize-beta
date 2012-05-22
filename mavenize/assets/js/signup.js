// Helper Functions
var getMavensUrl = function(page) {
  return '/mavens/' + page + '/';
}

$(document).ready(function() {
  // Initializer
  $('#mavens-container ul').loadUsers(getMavensUrl(1));

  // Listeners
  $('#btn-previous').click(function() {
    var previousPage = $('#mavens-container li:first').attr('data-previous');
    if (previousPage){
      $('#mavens-container ul').empty();
      $('#mavens-container ul').loadUsers(getMavensUrl(previousPage));
    }
  });

  $('#btn-next').click(function() {
    var nextPage = $('#mavens-container li:last').attr('data-next')
    if (nextPage) {
      $('#mavens-container ul').empty();
      $('#mavens-container ul').loadUsers(getMavensUrl(nextPage));
    }
  });

  $('#mavens-container ul').bind('appended', function() {
    var previousPage = $('#mavens-container li:first').attr('data-previous');
    var nextPage = $('#mavens-container li:last').attr('data-next')
    if (!previousPage)
      $('#btn-previous').attr('disabled', 'true');
    if (!nextPage)
      $('#btn-next').attr('disabled', 'true');
  });
});
