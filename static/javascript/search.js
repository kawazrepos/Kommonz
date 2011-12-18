(function() {
  $(function() {
    var $info;
    return $info = $('li.search-material li.info').click(function() {
      $(this).closest('li.search-material').find('article.material-info').toggle();
      return $(this).toggleClass('open');
    });
  });
}).call(this);
