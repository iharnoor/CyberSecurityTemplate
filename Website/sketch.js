function createCharts(response) {
    // alert(response);
    var twoLists = response.split('\n');
    var userAges = twoLists[0];
    var userNames = twoLists[1];

    var intAges = userAges.split`,`.map(x => +x);
    var stringNames = userNames.split(",");

    var linChart = new Chart(document.getElementById("lineChart"), {
        "type": "line",
        "data": {
            // "labels": ["January", "February", "March", "April", "May", "June", "July"],
            "labels": stringNames,
            "datasets": [{
                "label": "My First Dataset",
                "data": intAges,
                "fill": true,
                "borderColor": "rgb(75, 192, 192)",
                "lineTension": 0.1
            }]
        },
        "options": {responsive: true}
    });

    var pieData = {
        labels: stringNames,
        datasets: [{
            data: intAges,
            label: 'Points',
            backgroundColor: ['#f1c40f', '#e67e22', '#0092a0']
        }],
    };

    var pieChart = new Chart(document.getElementById("pieChart"), {
        "type": "pie",
        "data": pieData
    });
}


function onClickCreateGraph() {
    var input = null;
    var request = new XMLHttpRequest();

    request.addEventListener("readystatechange", function () {
        if (this.readyState === 4 && request.status === 200) {
            // alert(this.responseText);
            response = this.responseText;
            createCharts(response);
        } else {
            console.log(this.text);
        }
    });

    request.open("GET", "http://0.0.0.0:50/userAge");
    request.setRequestHeader("cache-control", "no-cache");
    request.send(input);
}
