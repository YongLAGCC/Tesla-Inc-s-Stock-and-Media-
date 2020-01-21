// Get the height of the footer on page load and resize, then add it as margin-bottom to the wrapper.
$(window).bind('load resize', function () {
    var footerHeight = $('#footer').outerHeight(true);
    $('#footer').css('height', footerHeight);
    $('#wrapper').css('margin-bottom', footerHeight);
});
