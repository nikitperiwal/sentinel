$(document).ready(function(){

	/* Date Field default values */
	function changeDateFormat(date){
		let dd = date.getDate();
		let mm = date.getMonth() + 1;
		let yyyy = date.getFullYear();
		if (dd < 10) dd = "0" + dd;
		if (mm < 10) mm = "0" + mm;
		date = yyyy + "-" + mm + "-" + dd;
		return date;
	}

	let start = new Date();
	let end = new Date();
	end.setDate(end.getDate()-7);

	$("#endDate").attr("value", changeDateFormat(start));
	$("#startDate").attr("value", changeDateFormat(end));

	/* Date Field validation */
	document.getElementById("startDate").addEventListener(
	    "change",
	    (funcName = function () {
	        startDateCheck("start");
	    }),
	    false
	);

	document.getElementById("endDate").addEventListener(
	    "change",
	    (funcName = function () {
	        startDateCheck("end");
	    }),
	    false
	);

	function startDateCheck(field) {
	    let startDate = $("#startDate").val();
	    let endDate = $("#endDate").val();
	    if (startDate > endDate) {
	      $.notify(
	        {
	          icon: "fas fa-calendar-alt",
	          message:
	            "Start date should be <b>lesser than or equal to</b> the End date.",
	        },
	        {
	          type: "danger",
	          timer: 5000,
	          placement: {
	            from: "top",
	            align: "right",
	          },
	        }
	      );
	      if (field == "start")
	        document.getElementById("startDate").value = endDate;
	      else document.getElementById("endDate").value = startDate;
	    }
	}


	/* Number Field validation */
	document.getElementById("dailyNum").addEventListener(
	    "focusout",
	    checkNumber
	);

	function checkNumber() {
	    let num = $("#dailyNum").val();
	    if (num < 0) {
	        $.notify(
	            {
	                icon: "fas fa-hashtag",
	                message: "The Daily tweet number should be greater than 0.",
	            },
	            {
	                type: "danger",
	            }
	        );
	        document.getElementById("dailyNum").value = 0;
	    } else if (num > 100) {
	        $.notify(
	        {
	            icon: "fas fa-hashtag",
	            message:
	            "The Daily tweet num should <b>not</b> be greater than 100.<br>Increase in daily tweet number will also lead to increase in time taken to scrape.",
	        },
	        {
	            type: "danger",
	        }
	        );
	    document.getElementById("dailyNum").value = 100;
	    }
	}
});

