new Chart(document.getElementById("line-chart"), {
  type: 'line',
  data: {
    labels: ["Apr 9", "Apr 10", "Apr 11", "Apr 12", "Apr 13", "Apr 14"],
    datasets: [{
        data: [43,23,42,12,34,27],
        label: "Positive",
        borderColor: "#3e95cd",
        fill: false
      },{
        data: [57,77,58,88,66,73],
        label: "Negative",
        borderColor: "#c45850",
        fill: false
      }
    ]
  },
  options: {
    title: {
      display: true,
      text: 'Sentiment of Columbia'
    }
  }
});
