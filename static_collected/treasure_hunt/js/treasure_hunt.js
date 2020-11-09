(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 71)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Scroll to top button appear
  $(document).scroll(function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 80
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Floating label headings for the contact form
  $(function() {
    $("body").on("input propertychange", ".floating-label-form-group", function(e) {
      $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
    }).on("focus", ".floating-label-form-group", function() {
      $(this).addClass("floating-label-form-group-with-focus");
    }).on("blur", ".floating-label-form-group", function() {
      $(this).removeClass("floating-label-form-group-with-focus");
    });
  });

  // Submit ajax post on submit answer
  $('#answer_form').on('submit', function(event){
    event.preventDefault();
    var url = $('#answer_form').attr('action');
    var answer = "";
    //If answer in one or multiple input
    $('input[name="input-answer"]').each(function( index ) {
      answer = answer  + $( this ).val().trim(); + " " ;
    });
    //if answer in list
    $('#answers_list').children('li').each(function( index ) {
      answer = answer  + $( this ).data("value");
    });

    answer = answer.trim();

    $.ajax({
      url : url,
      type : "POST", // http method
      data : { answer_input : answer}, // data sent with the post request

      // handle a successful response
      success : function(json) {
          $('#post-text').val(''); // remove the value from the input
          if(json == 'true'){
            $('#alert-success').removeClass('d-none');
            $('#alert-error').addClass('d-none');
            //Load the next answer button
            $('#button-next-puzzle').removeClass('d-none');
            //hide answer button
            $('#answer-button').addClass('d-none');
            //TODO to prevent cheating, the id of the next puzzle should come from json (but come on...)
            //$('#button-next-puzzle').href
          } else {
            $('#alert-error').removeClass('d-none');
            $('#alert-success').addClass('d-none');
            //TODO count ONE mistake when stat module implemented
          }
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error, please retry</div>"); // add the error to the dom
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
  });

  //Click on any hint button
  $('.btn-hint').click(function() {
    //Change the button colour
    $( this ).addClass('active');

    //log the click
    $.ajax({
      url : $( this ).data("url")  ,
      type : "POST", // http method
      data : { 
        type: 'hint_click',
        info: $( this ).data("hint-number"),
        place: $( this ).data("place") ,
        puzzle: $( this ).data("puzzle"),
              
      }, // data sent with the post request
      // handle a successful response
      success : function(json) {
        console.log('hint log successful'); 
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
  });

  //Click on any info button
  $('.btn-info').click(function() {
    //log the click
    $.ajax({
      url : $( this ).data("url")  ,
      type : "POST", // http method
      data : { 
        type: 'info_click',
        info: $( this ).data("hint-number"),
        place: $( this ).data("place") ,
        puzzle: $( this ).data("puzzle"),
              
      }, // data sent with the post request
      // handle a successful response
      success : function(json) {
        console.log('info log successful'); 
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
  });

  //Simple change language function
  $('.lang-link').click(function() {
    var next = $('#current-page').val().substr(3);
    var url = '/' + $(this).html().toLowerCase() + next;
    window.location = url;
  });

})(jQuery); // End of use strict

//For sortable lists
$(function() {
  $('.sortable').sortable();
});

/* CSRF TOKEN SECURITY*/
$(function() {

  // This function gets cookie with a given name
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  /*
  The functions below will create a header with csrftoken
  */

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  function sameOrigin(url) {
      // test that a given url is a same-origin URL
      // url could be relative or scheme relative or absolute
      var host = document.location.host; // host + port
      var protocol = document.location.protocol;
      var sr_origin = '//' + host;
      var origin = protocol + sr_origin;
      // Allow absolute or scheme relative URLs to same origin
      return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
          (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
          // or any other URL that isn't scheme relative or absolute i.e relative.
          !(/^(\/\/|http:|https:).*/.test(url));
  }

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
              // Send the token to same-origin, relative URLs only.
              // Send the token only if the method warrants CSRF protection
              // Using the CSRFToken value acquired earlier
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

});