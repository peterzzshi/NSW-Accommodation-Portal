
var token = $('#token').data()["name"];
var user_id = $('#user_id').data()["name"];


function deleteroom(object) {
    var id = object.id;
    $.ajax({
        url: 'http://13.210.33.67:5000/Item_operation?token=' + token + '&house_id=' + id,
        type: 'DELETE',
        success: function() {
            alert("listing deleted!");
            $("#" + id).parent().parent().remove();

        }
    });
}


function deletepost(object) {
    var id = object.id;

    $.ajax({
        url: 'http://13.210.33.67:5000/Posts?token=' + token + '&user_id=' + user_id + '&post_id=' + id,
        type: 'DELETE',
        success: function() {
            alert("Post deleted!");
            $("#" + id).parent().parent().remove();

        }
    });


}


function deletetrip(object) {
    var id = object.id;

    var url = 'http://13.210.33.67:5000/Confirm/User?token=' + token + '&user_id=' + user_id + '&transaction_id=' + id + "&status=cancel";

    $.ajax({
        url: url,
        type: 'POST',
        success: function() {
            object.disabled = true;
            $("#" + id).parent().parent().addClass("text-muted");
            alert("Trip cancelled!")
        }
    });
}


action("accept");
action("decline");


function action(status) {

    $("." + status).click(function () {

        var transaction_id = $(this).parent().parent().parent().attr('id')




        var data = {
            "token": token,
            "host_id": user_id,
            "transaction_id": transaction_id,
            "status": status
        };
        console.log(data);

        $.post("http://13.210.33.67:5000/Confirm/Host", data)
            .done(function (data) {
                console.log(data);
                // alert(status);
                if (status === "accept") {
                    alert("reservation accepted!");
                    // $(this).parent().children()[2].addClass("text-success");
                } else {
                    alert("reservation declined!");
                    // $(this).parent().children()[2].addClass("text-secondary");
                }
            })

    });
}













$('ul.nav li.dropdown').hover(function() {
    $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeIn(500);
}, function() {
    $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeOut(500);
});



$(document).ready(function() {

    var readURL = function(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.avatar').attr('src', e.target.result);
            };

            reader.readAsDataURL(input.files[0]);
        }
    }


    $(".file-upload").on('change', function(){
        readURL(this);
    });
});


