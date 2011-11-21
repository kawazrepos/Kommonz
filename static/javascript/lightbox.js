(function() {
  $(function() {
    var $uploadButton;
    $uploadButton = $('li.header-button-section a.upload-button');
    return $uploadButton.click(function(e) {
      var $container, $iframe, url;
      url = $(this).attr('href');
      $container = $('<div>').addClass('lightbox');
      $iframe = $('<iframe>');
      $iframe.attr('src', url);
      $('body').append($container);
      $container.append($("<div>").addClass('close')).append($iframe);
      $container.ready(function() {
        return $container.lightbox_me({
          closeClick: false,
          closeEsc: false
        });
      });
      return false;
    });
  });
}).call(this);
