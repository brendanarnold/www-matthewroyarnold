$(document).ready(function() {
  
  // The script for the slideshow code
  // see - http://stackoverflow.com/questions/18067062/
  $('.slideshow-link').click(function() {
    // Build an items list for use in Magnific Popup
    var items = [];
    $( $(this).attr('href') ).find('.slide').each(function() {
      items.push(
        { src : $(this) }
      );
    });
    $.magnificPopup.open({
      items: items,
      gallery: {
        enabled: true
      }
    });
    // Put this in here to prevent littering the history with URL
    // fragments - cancels the click event continuation
    return false;
  });

  // The script for positioning the background image flush to the right
  // of the main content container
  positionBgImgContainer();
  $(window).resize(function() {
    positionBgImgContainer();
  });
  function positionBgImgContainer() {
    var left = $('.row').offset().left + $('.row').width();
    $('#bg-container').css({'left': left - 400 + 'px', 'visibility': 'visible'});
  }

  // Set a behaviour so the opacity is decreaed when scrolling down to
  // allow reading of overlaid text
  setBGOpacity();
  $(window).scroll(setBGOpacity);
  $(window).resize(setBGOpacity);
  function setBGOpacity() {
    var pxFromTop = $(window).scrollTop();
    var fadeTo = 0.5;
    var vertPxTilFaded = 200;
    var opacity = (pxFromTop > vertPxTilFaded) ? fadeTo : 1 - fadeTo * (pxFromTop / vertPxTilFaded);
    $('#bg-container').css({'opacity': opacity});
  }

  // Put a smoother fade effect when hovering over the links
  $('.nav > a').mouseenter(function() {
      $(this).find('img').fadeTo(100, 0.7);
  })
  .mouseleave(function() {
      $(this).find('img').fadeTo(100, 1);
  });

});
