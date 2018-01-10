function isScrolledIntoView(elem)
{
    var $elem = $(elem);
    var $window = $(window);

    var docViewTop = $window.scrollTop();
    var docViewBottom = docViewTop + $window.height();

    var elemTop = $elem.offset().top;
    var elemBottom = elemTop + $elem.height();

    return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}

$(window).on('beforeunload', function() {
    $(window).scrollTop(0); 
});

$(document).ready(function() {

  $(window).fadeThis({
    offset:-150,
    speed:600,
  });

  // Fade effect
  $(".fadeMe").hide();
  $(".fadeMe").fadeToggle(555);

  var $window = $(window);
  // Parallax scrolling effect (blurryboston)
  $('div[data-type="background"]').each(function(){
    var $bgobj = $(this);
    $(window).scroll(function() {
      var yPos = -($window.scrollTop() / $bgobj.data('speed'));
      var coords = '50% '+ yPos + 'px';
      $bgobj.css({ 
        backgroundPosition: coords 
      });
    });
  });

  // Parallax scrolling effect (milling)
  $('section[data-type="background"]').each(function(){
    var $bgobj = $(this);
    var elemTop = $(this).offset().top;
    var offset =  456000 / $window.width();
    $(window).scroll(function() {
      var comp = $bgobj.css('padding-top');
      if(comp == '40px') {
        var yPos = -(($window.scrollTop()-elemTop) / $bgobj.data('speed'))-offset;
        var coords = '50% '+ yPos + 'px';
        $bgobj.css({ 
          backgroundPosition: coords 
        });
      }
    });
    $(window).resize(function() {
      var comp = $bgobj.css('padding-top');
      if(comp == '40px') {
        var yPos = -(($window.scrollTop()-elemTop) / $bgobj.data('speed'))-offset;
        var coords = '50% '+ yPos + 'px';
        $bgobj.css({ 
          backgroundPosition: coords 
        });
      }
    });
  });

  $(window).scroll(function() {
    if($window.scrollTop()>1000)
      $(document.getElementById("kakurenbou")).css('z-index', -1);
    else
      $(document.getElementById("kakurenbou")).css('z-index', 1);
  });
});