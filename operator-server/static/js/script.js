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
$('#input-name').typeahead({
  minLength: 1,
  highlight: true,
},
{
  name: 'companies',
  displayKey: 'name',
  source: companies.ttAdapter()
});

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

  // Focus forward/back
  $(".form-fields").on("focus", "input, textarea, .input", function() {
    var target = $(this).parent();
    target.addClass('active');
    target.removeClass('hidden');
    $.smoothScroll({
      offset: -focusHeight,
      scrollTarget: target,
    });
    console.log('focused.');
  });
  $('.form-fields .input').on('blur', function(e){
    console.log('input blur: parent removeClass active');
    $(this).parent().removeClass('active');
  });
  $('.form-fields label').on('click', function(e){
    console.log('click will result in focus.');
    $(this).next('.input').focus();
  });
  $('.form-fields .next').on('click', function(e){
    console.log('button click will result in focus.');
    $(this).parent().next('li').find('.input').first().focus();
  });
  $(document).on('typeahead:closed', function(){
    console.log('typeahead:closed');
    $('li.active').not('.hidden').last().next('li')
      .removeClass('hidden')
      .find('.input').focus();
  });
  $('.form-fields .input').bind('keyup', function(e){
    // Use [Up] and [Enter, Down]
    //   to iterative the form appropriately
    if(e.keyCode==38) {
      $(this).parent()
        .addClass('hidden')
        .prev('li').find('.input').focus();
    } else if(e.keyCode==13 || e.keyCode==40) {
      $(this).parent().next('li')
        .removeClass('hidden')
        .find('.input').focus();
    } 
  });

  // Initialize state
  var focusHeight = $('.form-fields input').first().offset().top;
  console.log('focusHeight = ' + focusHeight);
  $('.form-fields input').first().focus();

  // Submit data
  $('#submit').on('click', function(e){

    // Build the payload
    var payload = {};
    $('form#app').find("input, textarea, .input").each(function() {
      payload[this.name] = $(this).val();
    });
    payload.sequence = payload['1'];
    payload = JSON.stringify(payload);

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
    })
    .fail(function(response) {
      console.log('fail.');
    })
    .always(function(response) {
      console.log('request: '  + payload);
      console.log('response: ' + response);
    });

  });

});

// Google Analytics
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');
ga('create', 'UA-10935216-9', 'happyoperator.com');
ga('send', 'pageview');