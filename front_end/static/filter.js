var keyword = $('#keyword').data()["name"];

var items = $(".search-items");

$("#filter").click(function () {
    for (var i = 0; i < items.length; i++) {
        items[i].hidden = false;
    }

    var start_date, end_date, price_start, price_end;
    var searchinfo = $("#rooms-search").serializeArray();
    var url = "http://13.210.33.67:5000/Search?key_word=" + keyword;

    if (searchinfo.length === 4) {
        start_date = searchinfo[0].value;
        end_date = searchinfo[1].value;
        price_start = searchinfo[2].value;
        price_end = searchinfo[3].value;
        if (start_date && end_date) {
            url = url + "&start_date=" + start_date + "&end_date=" + end_date;
        }
        if (price_start && price_end) {
            url = url + "&price_start=" + price_start + "&price_end=" + price_end;
        }
    } else if (searchinfo.length === 5) {
        start_date = searchinfo[0].value;
        end_date = searchinfo[1].value;
        var type = searchinfo[2].value;
        price_start = searchinfo[3].value;
        price_end = searchinfo[4].value;

        if (start_date && end_date) {
            url = url + "&start_date=" + start_date + "&end_date=" + end_date;
        }
        url = url + "&type=" + type;
        if (price_start && price_end) {
            url = url + "&price_start=" + price_start + "&price_end=" + price_end;
        }
    }

    $.get(url)
        .done(function (data) {
            var ids = [];
            for (var i = 0; i < data["items"].length; i++) {
                ids.push(data["items"][i].id);
            }

            for (var i = 0; i < items.length; i++) {
                if (ids.indexOf(parseInt(items[i].id)) === -1) {
                    items[i].hidden = true;
                }
            }
        });
})