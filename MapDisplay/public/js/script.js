const sentimentValues = new Array()
const sentimentDates = new Array()

function getData(callback) {
  $.ajax({url: '/api/coordinates', success: callback});
}

function createMap(data) {
  var parsedData = data.data;
  parsedData.forEach(function(element) {
    sentimentValues.push(element.value)
    sentimentDates.push(element.date.substring(4,10))
  });

  var ctx = document.getElementById("line-chart").getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: sentimentDates,
      datasets: [{
          data: sentimentValues,
          label: "sentiment values",
          borderColor: "#0f0f0a",
          fill: false
        },
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Sentiment of Columbia'
      }
    }
  });
}

getData(createMap)
