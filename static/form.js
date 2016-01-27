$(document).ready(function() {
	$('#loading').hide();
})

function getFormData() {
	var objs = $('form').serializeArray();
	reqData = {};
	for (var i = 0; i < objs.length; i++) {
		var name = objs[i]['name'];
		var value = objs[i]['value'];
		reqData[name] = $.trim(value);
	}

	if ((reqData['firstname'] == '') || (reqData['lastname'] == '')) {
		if (reqData['firstname'] == '') {
			$('#firstname').css({'background-color': '#FFB2B2'});
		}
		if (reqData['lastname'] == '') {
			$('#lastname').css({'background-color': '#FFB2B2'});
		}
	}
	else {
		$.ajax({
			type: 'POST',
			url: 'results',
			data: reqData,
			dataType: 'json',
			beforeSend: clearScreen,
			success: showData
		});
	}

	function clearScreen() {
		$('form').fadeOut(
			function() {
				$('#loading').fadeIn();
			}
		);
	}

	function showData(data) {
		$('#loading').fadeOut();
		var emails = []
		var confidence = [];
		for (var i = 0; i < data['results'].length; i++) {
			emails.push(data['results'][i][0]);
			confidence.push(data['results'][i][1]);
		}

		var maxConfidence = Math.max(...confidence);
		for (var i = 0; i < confidence.length; i++) {
			confidence[i] = Math.round((confidence[i]/maxConfidence) * 100);
			$('#ratings').append('<span class="email" id="email' + i.toString() + '" >' + confidence[i].toString() + '</span>');
		}

		for (var i = 0; i < emails.length; i++) {
			$('#email' + i.toString()).barIndicator({
				forceAnim: true,
				horTitle: emails[i],
				horLabelPos: 'topRight',
				colorRange:true,
				colorRangeLimits: {
					optimal: '91-100',
					newRangeOne: '61-90-rgb(241,144,40)',
					newRangeTwo: '41-60-green',
					newRangeThree: '21-40-#4aa64f',
					critical: '0-20'
				}
			});
		}
	}
}