$(document).ready(function() {
  /* Requires jQuery Forms (jquery.forms.js) and Rating Form
     (ratingForm.js)
   */
  var selectedReview;
  $('.modal').hide();

  // Templates
  var raveTemplate = _.template("\
    <div class='modal-header'>\
      <a class='close' data-dismiss='modal'>×</a>\
      <h3>Disagree? Leave your own rave.</h3>\
    </div>\
    <div class='modal-body'>\
      <form class='form-horizontal' action='<%= postUrl %>' method='POST'>\
        <%= csrfField %>\
        <textarea id='modal-text' placeholder='Tell us what you thought, choose a rating, and rave!' rows='1' name='text'></textarea>\
        <div class='btn-group' id='modal-rating' data-toggle='buttons-radio'>\
          <% for (var i = 0; i < 4; i++) { %>\
            <button class='btn' type='button' name='rating' value='<%= i %>'>\
              <img src='<%= smileyUrls[i] %>'/>\
            </button>\
          <% } %>\
        </div>\
        <button class='btn btn-large btn-primary disabled' id='modal-submit' type='submit' name='rating' value='0' disabled='true'>\
          Rave\
        </button>\
        <div style='clear: both;'></div>\
      </form>\
    </div>");

  var thankTemplate = _.template("\
    <div class='modal-header'>\
      <a class='close' data-dismiss='modal'>×</a>\
      <h3>Leave a thank you note (optional).</h3>\
    </div>\
    <div class='modal-body'>\
      <form class='form-horizontal' action='<%= postUrl %>' method='POST'>\
        <%= csrfField %>\
        <textarea id='modal-text' placeholder='You are awesome because...' rows='1' name='text'></textarea>\
        <button class='btn btn-large btn-primary' id='modal-submit' type='submit'>\
          Thank\
        </button>\
      </form>\
    </div>");

  // Helper Functions
  var disagreeUrl = function(reviewId) {
    return '/disagree/' + reviewId + '/';
  }

  var thankUrl = function(reviewId) {
    return '/thank/' + reviewId + '/';
  }

  var smileyUrl = function(rating) {
    return STATIC_URL + 'img/' + rating + 's.png';
  }

  // Listeners
  $('.review a[data-toggle="modal"]').click(function() {
    selectedReview = $(this).closest('.review').val();
  });

  $('.activities').bind('appended', function() {
    $('a[data-toggle="modal"]').click(function() {
      selectedReview = $(this).closest('.activity').val();
    });
  });

  $('#disagree').on('show', function() {
    var form = raveTemplate({
      postUrl: disagreeUrl(selectedReview),
      csrfField: CSRF_FIELD,
      smileyUrls: [smileyUrl(1), smileyUrl(2), smileyUrl(3), smileyUrl(4)]
    });
    $(this).append(form);
    $('#modal-text').elastic();
    $(this).find('form').ajaxForm();
    $(this).find('form').ratingForm();
  });

  $('#thank').on('show', function() {
    var form = thankTemplate({
      postUrl: thankUrl(selectedReview),
      csrfField: CSRF_FIELD,
    });
    $(this).append(form);
    $('#modal-text').elastic();
    $(this).find('form').ajaxForm();
  });

  $('.modal').on('hide', function() {
    $(this).empty();
  });
});
