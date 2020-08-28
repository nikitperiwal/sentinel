
$(document).ready(function(){
  //	Sentiment Chart
	new Chart(document.getElementById("chart-timeline-sentiment"), {
    type: 'line',
    data: {
      datasets: [{
            label: "Short Term Sentiment",
            data: short_sentiment,
            borderColor: "indianred",
            backgroundColor: "indianred",
            fill: false,
            pointRadius: 0,
            lineTension: 0,
            borderWidth: 2,
        },{
            label: "Long Term Sentiment",
            data: long_sentiment,
            borderColor: "slateblue",
            backgroundColor: "slateblue",
            fill: false,
            pointRadius: 0,
            lineTension: 0,
            borderWidth: 2,
        }]
    },
    options: {
	    responsive: true,
	    maintainAspectRatio: false,
	    legend: {
	      display: true,
	    },
      scales: {
        xAxes: [{
          type: "time",
          distribution: "series",
          time: {
            unit: 'day',
            tooltipFormat: "MMM D h:mm a",
            displayFormats: {
              day: 'MMM D'
            },
          },
          ticks: {
            display: false,
          },
          gridLines: {
            drawTicks: false,
            display: false,
            drawBorder: false,
          },
        }],
        yAxes: [{
          ticks: {
	          min: -1,
	          max: 1,
	          maxTicksLimit: 5,
          },
        }]
      },
      tooltips: {
	      intersect: false,
	      mode: 'index',
      }
    }
  });


//	Volume Chart
	new Chart(document.getElementById("chart-timeline-volume"), {
    type: 'bar',
    data: {
      datasets: [{
            label: "Volume",
            data: volumedata,
            backgroundColor: "teal"
        }]
    },
    options: {
	    responsive: true,
	    maintainAspectRatio: false,
	    legend: {
	      display: false,
	    },
      scales: {
        xAxes: [{
          type: "time",
          time: {
            unit: 'day',
            tooltipFormat: "MMM D h:mm a",
            displayFormats: {
              day: 'MMM D'
            },
          },
          ticks: {
            padding: 10,
          },
          gridLines: {
            drawTicks: false,
            display: false,
            drawBorder: false,
          },
        }],
        yAxes: [{
          ticks: {
            beginAtZero: true,
            padding: 8,
          }
        }]
      },

      tooltips: {
	    intersect: false,
	    mode: 'index',
      }
    }
  });
});