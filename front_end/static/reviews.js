var starbase = "<ul class='display'><li class='star' data-value='1'><i class='fa fa-star fw'></i></li> <li class='star' data-value='2'><i class='fa fa-star fw'></i></li><li class='star' data-value='3'><i class='fa fa-star fw'></i></li><li class='star' data-value='4'><i class='fa fa-star fw'></i></li><li class='star' data-value='5'><i class='fa fa-star fw'></i></li></ul>"

var home_id = $('#home_id').data()["name"];
var token = $('#token').data()["name"];
var user_id = $('#user_id').data()["name"];
var user_name = $('#user_name').data()["name"];

var ratinginput = 5;


var reviewinput, transaction_id;

$(document).ready(function() {

    $.getJSON("http://13.210.33.67:5000/Trip?token=" + token + "&user_id=" + user_id, function (data) {
        var trips = data["transaction"];
        for (var i = 0; i < trips.length; i++) {
            if (trips[i]["house_id"] === home_id) {
                transaction_id = trips[i]["transaction_id"];
            }
        }
    });


    $.getJSON("http://13.210.33.67:5000/Review?item_id=" + home_id, function (data) {
        var reviews = data["review"];
        for (var i = 0; i < reviews.length; i++) {
            addReview(reviews[i]["user_id"], reviews[i]["comment"]);
            // addRating(reviews[i]["user_id"], reviews[i]["value"]);
        }

    });




    /* 1. Visualizing things on Hover - See next part for action on click */
    $('.rating li').on('mouseover', mouseover).on('mouseout', mouseout);


});


/* 2. Action to perform on click */
$('.rating li').click(function() {
    const onStar = parseInt($(this).data('value'), 10); // The star currently selected
    const stars = $(this).parent().children('li.star');

    for (var i = 0; i < stars.length; i++) {
        $(stars[i]).removeClass('selected');
    }

    for (var i = 0; i < onStar; i++) {
        $(stars[i]).addClass('selected');
    }
    ratinginput = parseInt($('.rating li.selected').last().data('value'), 10);

});


$("#submit-review").click(function () {
    reviewinput = $("#reviewInput").val();
    if (ratinginput == null)  {
        alert("Please give a rating");
    } else if (reviewinput == null || reviewinput.match(/^ *$/) !== null){
        alert("Invalid input, a review should not contain only spaces");
    } else {
        console.log(reviewinput);
        console.log(ratinginput);
        createReview(reviewinput, ratinginput);

        addReview(user_id, reviewinput);
        // addRating(user_id, ratinginput);
    }


    $('.success-box').fadeIn(200);
    $('.success-box div.text-message').html("<span> Thank you for your feedback </span>");


    $("#review *").prop('disabled',true);
})




function addReview(id, review) {
    const newReview = $("<li>" + review + "<span class='stars text-center' id=" + id + "></span> By " + user_name + "</li>");
    $('#reviews').append(newReview);
    $("#reviewInput").val("");

}


function addRating(id, rating) {
    $('span#' + id).html(starbase);
    var stars = $("#" + id + " li");
    for (var i = 0; i < rating; i++) {
        $(stars[i]).addClass('selected');
    }
}


function today() {
    var today = new Date();
    var day = today.getDate();
    var month = today.getMonth() + 1;
    var year = today.getFullYear();

    if (day < 10) {
        day = '0' + day;
    }
    if (month < 10) {
        month = '0' + month;
    }
    return year + '-' + month + '-' + day;
}



function createReview(reviewinput, ratinginput) {

    var data = {
        token: token,
        user_id: user_id,
        transaction_id: transaction_id,
        date: today(),
        comment: reviewinput,
        communication : ratinginput,
        accuracy : ratinginput,
        cleanliness : ratinginput,
        location : ratinginput,
        check_in : ratinginput,
        value : ratinginput
    }
    $.post('http://13.210.33.67:5000/Review', data
    )
        .done(function (data) {
            console.log(data);

        })
        .fail(function (data) {
            console.log(data);
        })


}





function mouseover() {
    const onStar = parseInt($(this).data('value'), 10); // The star currently mouse on

    // Now highlight all the stars that's not after the current hovered star
    $(this).parent().children('li.star').each(function(e){
        if (e < onStar) {
            $(this).addClass('hover');
        }
        else {
            $(this).removeClass('hover');
        }
    });
}

function mouseout() {
    $(this).parent().children('li.star').each(function(){
        $(this).removeClass('hover');
    });
}