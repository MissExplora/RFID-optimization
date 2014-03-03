var levels = [
    {
      "name": "progress-bar-info",
      "qty": 2
    },
    {
      "name": "progress-bar-success",
      "qty": 5
    },
    {
      "name": "progress-bar-warning",
      "qty": 9
    },
    {
      "name": "progress-bar-danger",
      "qty": 999
    },
];


function findLevel(count) {
    for (i in levels) {
        var level = levels[i];
        if (count < level.qty) {
            return level.name;
        }
    }
}

$(function () {
    $.get("http://127.0.0.1:8080/kos", function (data) {
        console.log($('table'));

        var maxcount = -1;
        for (i in data) {
            var row = data[i];
            if (row.count > maxcount) {
                maxcount = row.count;
            }
        }

        for (i in data) {
            var dom = $(".template.pinky").clone().removeClass("template");
            var row = data[i];

            $(".var_blagajna", dom).text(row.blagajna);

            $(".var_count", dom).text(row.count);
            $(".var_count_progress", dom).css("width", parseInt(100*row.count/maxcount) + "%");
            $(".var_count_progress", dom).addClass(findLevel(row.count));

            console.log(row.count, findLevel(row.count));

            $('table').append(dom);
        }
    });
});

