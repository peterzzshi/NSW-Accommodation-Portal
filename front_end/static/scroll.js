$(document).ready(function() {
    var baseurl = "http://13.210.33.67:5000/Home_page?page_number=";
    var page_number = 2;
    var status = 1;

    $(window).scroll(function() {
        // End of the document reached?
        if ($(document).height() - $(window).height() == $(window).scrollTop()) {
            var url = baseurl + page_number;
            page_number++;

            if (status === 1) {
                $.get(url, function(data) {
                    var items = data.items;
                    if (data.exist_next_pages === 0) {
                        status = 0;
                        $('#loading').html('<h3>No more...</h3>').show();
                    }
                    else {
                        $('#loading').html('<h3>Loading...</h3>').show();
                        for (var i = 0; i < items.length; i++) {
                            $('#rooms').append(generate_item(items[i]));
                        }
                        $('#loading').hide();
                    }
                });
            }
        }
    });
});


function generate_item(item) {

    var atag =  '<a href="rooms/' + item.id + '">'
    var markup = '<div class="col-4"><figure>';
    markup += atag;
    markup += '<img src='+ item.image + ' alt="">'
    markup += atag;
    markup += '<figcaption>' + item.name + ' $' + item.price + '</figcaption>';

    if (item.rating_number === 0) {
        markup += '</a><span>Newly launched listing</span>';
    } else {
        markup += '</a><span>' +item.rating_number + 'people rated, with mean rating' + item.rating

    }
    markup += '</span></figure></div>';

    return markup

}