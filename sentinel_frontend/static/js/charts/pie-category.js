$(document).ready(function(){
	new Chart(document.getElementById("chart-pie"), {
	  type: "pie",
	  data: {
	    labels: ["Positive", "Negative"],
	    datasets: [
	      {
	        backgroundColor: ["#3cba9f", "#3e95cd"],
	        data: pie_data,
	      },
	    ],
	  },
	  options: {
	    responsive: true,
	    maintainAspectRatio: false,
	    legend: {
	      display: true,
	      position: "right",
	      labels: {
	        fontColor: "rgb(180, 180, 180)",
	        fontSize: 14,
	      },
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
	            display: false,
	          },
	          gridLines: {
	            display: false,
	            drawBorder: false,
	          },
	        },
	      ],
	      xAxes: [
	        {
	          ticks: {
	            display: false,
	          },
	          gridLines: {
	            display: false,
	            drawBorder: false,
	          },
	        },
	      ],
	    },
	    layout: {
	      padding: {
	        left: 0,
	        right: 0,
	        top: 0,
	        bottom: 0,
	      },
	    },
	  },
	});
});