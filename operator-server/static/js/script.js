/**
 * script.js
 * HappyOperator.com
 */


// Typeahead
var companies = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: '/companies/search/%QUERY'
});
companies.initialize();
$('#outbound').typeahead({
  minLength: 1,
  highlight: true,
},
{
  name: 'companies',
  displayKey: 'name',
  source: companies.ttAdapter()
});

var sequence = [];

function appendOptions (event) {
  $(event.target).parent().nextAll().remove()
  sequence = sequence.slice(0, $(this).parent().index() - 3);
  sequence.push($(this).find('span.num').html());
  var options = $(this).data('options');
  console.log('unpack options', options);
  if (options) {
    var op_li = $('<li/>').addClass('optgroup');
    for (var option in options) {
      var new_a = $('<a href="#"><span class="num">'+options[option].button+'</span> '+options[option].title+'</a>').data('options', options[option].options).click(appendOptions);
      new_a.appendTo(op_li);
    }
    $('ul.form-fields').append(op_li);
  }
  else {
    optionsComplete();
  }
  event.preventDefault();
  return false;
}

function optionsComplete() {
  var new_button = $('<li><label></label><a href="#" class="text-input btn btn-primary" id="submit">Call me <span class="entypo chevron-right"></span></a></li>');
  new_button.appendTo('ul.form-fields');

  // Submit data
  $('#submit').on('click', function(e){

    // Build the payload
    var payload = {};
    $('form#app').find("input, textarea, .text-input").each(function() {
      payload[this.name] = $(this).val();
    });
    payload['phone'] = '+1 ' + payload['phone'];
    payload['sequence'] = sequence;
    payload = JSON.stringify(payload);

    // Hide field entry
    $('#intro').fadeOut();
    $('.form-fields li').each(function(){ $(this).fadeOut(); });

    // POST to the application
    var jqxhr = $.ajax({
      type: 'POST',
      url: '/outbound/new',
      contentType: "application/json;charset=UTF-8",  // request
      data: payload,
      accepts: "application/json",  // response
      cache: false
    })
    .done(function() {
      console.log('done.');
      $('.wrapper').append("<p>Got it! I'll give you a call when they're ready. And keep an eye on your email for the transcript.</p>");
    })
    .fail(function(response) {
      console.log('fail.');
      $('.form-fields li').each(function(){ $(this).fadeIn(); });
      $('.form-fields li').last().append("<label>Something bad happened :(</label>");
    })
    .always(function(response) {
      console.log('request: '  + payload);
      console.log('response: ' + response);
    });


  });

}

// Serialize form for submission as JSON object.
//   Snippet via http://jsfiddle.net/sxGtM/3/
$.fn.serializeObject = function(){
  var o = {};
  var a = this.serializeArray();
  $.each(a, function() {
    if (o[this.name] !== undefined) {
      if (!o[this.name].push) {
          o[this.name] = [o[this.name]];
      }
      o[this.name].push(this.value || '');
    } else {
      o[this.name] = this.value || '';
    }
  });
  return o;
};

$(document).ready(function(){

  // Faster scrolling
  //   via <thecssninja.com/javascript/pointer-events-60fps>.
  var body = document.body, timer;
  window.addEventListener('scroll', function(){
    clearTimeout(timer);
    if(!body.classList.contains('disable-hover'))
      body.classList.add('disable-hover')
    timer = setTimeout(function(){
      body.classList.remove('disable-hover')
    }, 500);
  }, false);

  // General focus forward/back
  $("form#app li").focusin(function(){
    $(this).removeClass('hidden');
    $(this).addClass('active');
    var target = $(this).find('.text-input').first();
    $.smoothScroll({
      offset: -focusHeight,
      scrollTarget: target,
      afterScroll: focus(target),
      speed: 200
    });
    $(this).nextAll('li').addClass('hidden');
    console.log('form#app li focusin() done.')
  });
  $("form#app li").focusout(function(){
    $(this).removeClass('active');
    console.log('form#app li focusout() done.')
  });

  // Focus forward/back
  /*
  $(".form-fields").on("focus", ".text-input", function(){
    var target = $(this).parent('li');
    target
      //.removeClass('hidden')
      .nextAll('li').addClass('hidden');
    $.smoothScroll({
      offset: -focusHeight,
      scrollTarget: target,
      speed: 200
    });
    target.addClass('active')
    console.log('focused.');
  });
  */
  /*
  $('.form-fields .text-input').on('blur', function(e){
    console.log('.text-input blur: parent removeClass active');
    $(this).parent().removeClass('active');
  });
  */
  /*
  $('.form-fields label').on('click', function(e){
    console.log('click will result in focus.');
    $(this).next('.text-input').focus();
  });
  */
  $('.form-fields .next').on('click', function(e){
    console.log('button click will result in focus.');
    $(this).parentsUntil('li.active').first().parent()
      .next('li.hidden .text-input').focus();
  });
  $(document).on('typeahead:opened', function() {
    $('.company-not-found').html("");
  });
  $(document).on('typeahead:closed', function(){
    console.log('typeahead:closed');
    $('li.active').removeClass('active')
      .next('li').find('.text-input').first()
      .focus();

    /* Begin bad code */
    var company_name = $('#outbound').val();
    $(this).next('li').removeClass('hidden');
    $.getJSON('/companies/info/' + company_name, function (data) {
      if (data.error) {
        $('.company-not-found').html("No data found for this company.");
      }
      var options = data.options;

      if (options) {
        var op_li = $('<li/>').addClass('optgroup');
        op_li.append('<label>Please select an option:</label>');
        for (var option in options) {
          console.log('op3', options[option].options);
          var new_a = $('<a href="#"><span class="num">'+options[option].button+'</span> '+options[option].title+'</a>').data('options', options[option].options).click(appendOptions);
          new_a.appendTo(op_li);
        }
        $('ul.form-fields').append(op_li);
      }
      else {
        optionsComplete();
      }
    });
    /* End bad code */

  });
  $('.form-fields .text-input').bind('keydown', function(event){
    if((event.keyCode==9 && event.shiftKey) || event.keyCode==38) {
      // Use [Shift+Tab, Up] to iterate up.
      //$(this).parent().trigger('focusout');
      $(this).parent().prev('li').trigger('focusin');
      //event.preventDefault();
    } else if(event.keyCode==9 || event.keyCode==13 || event.keyCode==40) {
      // Use [Tab, Enter, Down] to iterate down.
      var dataNext = $(this).data('next');
      console.log(dataNext);
      if(!(dataNext=="")) {
        $(this).parent().trigger('focusout');
        //$('li.hidden').first().removeClass('hidden');
        $(dataNext).trigger('focusin');
      } else {
        //$(this).parent().trigger('focusout');
        console.log($(this).parent().next('li'));
        $(this).parent().next('li').trigger('focusin');
      }
      //event.preventDefault();
    } 
  });

  // Initialize state
  var focusHeight = $('.form-fields input').first().offset().top;
  console.log('focusHeight = ' + focusHeight);
  //$('form#app>ul>li').addClass('.hidden');
  $('form#app>ul>li').first()
    .removeClass('.hidden')
    .addClass('active');
  $('form#app .text-input').first().focus();

  // Mask input
  $("[type='tel']").mask("(999) 999-9999", {placeholder: " ", completed: function(){
    $(this).parent().next('li')
      .removeClass('hidden')
      .find('.text-input').first().focus();
  }});

});

// Google Analytics
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');
ga('create', 'UA-10935216-9', 'happyoperator.com');
ga('send', 'pageview');