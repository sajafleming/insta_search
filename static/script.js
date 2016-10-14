"use strict";
$(document).ready(function () {

  // get values form values and make instagram request when user submits
  $('#user-input-form').submit(function(evt) {
    // preventDefault of going to a new page (since POST request)
    evt.preventDefault()

    // clear existing photos on page
    $('#pictures').empty()

    // get values from user textboxes
    var tag = $('#tag').val();
    var start_date = $('#start_date').val();
    var end_date = $('#end_date').val();

    console.log(tag, start_date, end_date)
   
    // set the params for the instagram query
    var params = {"tag": tag, "start": start_date, "end": end_date};

    // ajax call to get pictures, along with success funct to show pics
    $.get("search-insta", params, showPictures);

  });

  
  function showPictures(data) {

    // number of pics returned
    var picturesLength = data.pic_urls.length;

    if (picturesLength == 0) {
      // if there are no pictures, alert the user
      alert("no results, try a different tag")

    } else {

      // loop through pictures and create img tags to add to html
      for (var i = 0; i < picturesLength; i++) {

        var pic = data.pic_urls[i]
        console.log(pic)
        var html = '<img id="img" src="';

        html += pic + '" />';
      
        console.log(html)

        $('#pictures').prepend(html);

      }
      
    }

  }



});