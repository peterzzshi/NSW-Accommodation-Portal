var home_id = $('#home_id').data()["name"];
var hoster_id = $('#hoster_id').data()["name"];


var token = $('#token').data()["name"];
var user_id = $('#user_id').data()["name"];


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


var xcheckin;
$.get("http://13.210.33.67:5000/Unavailable_date?house_id=" + home_id)
    .done(function (data) {
        xcheckin = data["unavailable"];
    });


var xcheckout;
var day, month, year;

$('#checkin-date.avalCall').datepicker({
    beforeShowDay: function(date){
        var string = jQuery.datepicker.formatDate('yy-mm-dd', date);
        return [ xcheckin.indexOf(string) == -1 ]
    },
    minDate: new Date(),
    onSelect: function () {
        var checkin_date = $("#checkin-date").val();
        console.log(checkin_date);
        year = checkin_date.split("/")[2];
        month = checkin_date.split("/")[0];
        day = checkin_date.split("/")[1];
        checkin_date = year  + "-" + month + "-" + day;

        $.get("http://13.210.33.67:5000/Unavailable_date?house_id=" + home_id + "&start_date=" + checkin_date)
            .done(function (data) {
                xcheckout = data["unavailable"];
                console.log(xcheckout);
            });
    }
});



$('#checkout-date.avalCall').datepicker({
    beforeShowDay: function(date){
        var string = jQuery.datepicker.formatDate('yy-mm-dd', date);
        return [ xcheckout.indexOf(string) == -1 ]
    },
    minDate: new Date()

});




$("#submit_dates").click(function () {
    var checkin = $("#checkin-date").val();
    var checkout = $("#checkout-date").val();

    console.log(checkin, checkout);

    if (checkin == null || checkin.match(/^ *$/) !== null || checkout == null || checkout.match(/^ *$/) !== null) {
        alert("Please complete the check in and check out dates before proceeding.");
    } else {
        checkin = checkin.split("/");
        checkout = checkout.split("/");
        var start_date = checkin[2] + '-' + checkin[0] + '-' + checkin[1];
        var end_date = checkout[2] + '-' + checkout[0] + '-' + checkout[1];


        var data = {
            "token": token,
            "item_id": home_id,
            "host_id": hoster_id,
            "user_id": user_id,
            "date": today(),
            "start_date": start_date,
            "end_date": end_date,
            "comment": "string"
        };

        console.log(data);


        $.post("http://13.210.33.67:5000/Book", data)
            .done(function (a, b, c){
                alert("Booking completed!");

                console.log(a);
                console.log(b);
                console.log(c);

            })
            .fail(function (a, b, c) {
                alert("failed!");
                console.log(a);
                console.log(b);
                console.log(c);
            })
    }

});