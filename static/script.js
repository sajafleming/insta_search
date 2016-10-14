"use strict";
$(document).ready(function () {

  // get values from user text boxes
  $('#user-input-form').submit(function(evt) {
    evt.preventDefault()

    console.log('got here')

    var tag = $('#tag').val();
    var start_time = $('#start_time').val();
    var end_time = $('#end_time').val();
   
    // get the params for the instagram query
    var params = {"tag": tag, "start": start_time, "end": end_time};

    // ajax call to get pictures
    $.get("search-insta", params, showPictures);

  });

  
  function showPictures(data) {

    console.log(data)

    var picturesLength = data.pic_urls.length;

    if (picturesLength == 0) {
      alert("no results with that tag")
    } else {

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