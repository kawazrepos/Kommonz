(function() {
  $(function() {
    var $info;
    return $info = $('li.list-material li.info').click(function() {
      $(this).closest('li.list-material').find('article.material-info').toggle();
      return $(this).toggleClass('open');
    });
  });
}).call(this);
