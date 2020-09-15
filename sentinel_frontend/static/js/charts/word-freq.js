$(document).ready(function(){
	new Chart(document.getElementById("chart-word-frequency"), {
	  type: "horizontalBar",
	  data: {
	    labels: positive_name,
	    datasets: [
	      {
	        backgroundColor: "#3cba9f",
	        data: positive_freq,
	      },
	    ],
	  },
	  options: {
	    responsive: true,
	    maintainAspectRatio: false,
	    legend: {
	      display: false,
	    },
	    tooltips: {
	      bodySpacing: 4,
	      mode: "nearest",
	      intersect: 0,
	      position: "nearest",
	      xPadding: 10,
	      yPadding: 10,
	      caretPadding: 10,
	    },
	    scales: {
	      yAxes: [
	        {
	          ticks: {
	            display: true,
	            min: 0,
	          },
	          gridLines: {
	            display: true,
	            drawTicks: false,
	            drawBorder: false,
	          },
	        },
	      ],
	      xAxes: [
	        {
	          ticks: {
	            display: true,
	            padding: 10,
	            fontSize: 13,
	          },
	          gridLines: {
	            drawTicks: false,
	            display: false,
	            drawBorder: false,
	          },
	        },
	      ],
	    },
	    layout: {
	      padding: {
	        left: 2,
	        right: 2,
	        top: 10,
	        bottom: 10,
	      },
	    },
	  },
	});
});