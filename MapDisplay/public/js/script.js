const sentimentValues = new Array()
const sentimentDates = new Array()

function getData(callback) {
  $.ajax({url: '/api/coordinates', success: callback});
}

function createMap(data) {
  var parsedData = data.data;
  parsedData.forEach(function(element) {
    sentimentValues.push(element.value)
    sentimentDates.push(element.date.substring(10,19))
  });

  Chart.defaults.global.defaultFontColor = "#ffffff";

  var ctx = document.getElementById("line-chart").getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: sentimentDates.slice(-250),
      datasets: [{
        data: sentimentValues.slice(-250),
        label: "sentiment values",
        borderColor: "#6ABEDB",
        fill: false
      },
    ]
  },
  options: {
    title: {
      display: true,
      text: 'Sentiment of Columbia'
    },
    scales: {
      xAxes: [{
        ticks: {
          maxTicksLimit: 100,
        }
      }]
    }
  }
});
}

getData(createMap)
