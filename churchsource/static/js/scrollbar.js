$(function() {
  var win = $(window);
  // Full body scroll
  var isResizing = false;
  win.bind(
    'resize',
    function()
    {
      if (!isResizing) {
        isResizing = true;
        var container = $('#mainWrapper.touch');
        // Temporarily make the container tiny so it doesn't influence the
        // calculation of the size of the document
        container.css(
          {
            'width': 1,
            'height': 1
          }
        );
        // Now make it the size of the window...
        container.css(
          {
            'width': win.width(),
            'height': win.height()
          }
        );
        isResizing = false;
        container.jScrollPane(
          {
            'showArrows': true
          }
        );
      }
    }
  ).trigger('resize');

  // Workaround for known Opera issue which breaks demo (see
  // http://jscrollpane.kelvinluck.com/known_issues.html#opera-scrollbar )
  $('body').css('overflow', 'hidden');

  // IE calculates the width incorrectly first time round (it
  // doesn't count the space used by the native scrollbar) so
  // we re-trigger if necessary.
  if ($('#mainWrapper.touch').width() != win.width()) {
    win.trigger('resize');
  }
});
