$(document).ready(function(){
	new Chart(document.getElementById("chart-bar"), {
	  type: "bar",
	  data: {
	    labels: ["Positive", "Negative", "All tweets"],
	    datasets: [
	      {
	        backgroundColor: ["#3cba9f", "#3e95cd", "#8e5ea2"],
	        data: bar_data,
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