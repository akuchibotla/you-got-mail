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

	if (reqData['domains']) {
		reqData['domains'] = reqData['domains'].replace(/ /g,'')
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
		$('#loading').fadeOut(function() {
			setTimeout(showBars(data), 1000)
		});
	}

	function showBars(data) {
		var emails = []
		var confidence = [];
		for (var i = 0; i < data['results'].length; i++) {
			emails.push(data['results'][i][0]);
			confidence.push(data['results'][i][1]);
		}

		var maxConfidence = Math.max(...confidence);
		$('#ratings').append('<a id="search" href="/">Search Again</a>')

		for (var i = 0; i < confidence.length; i++) {
			confidence[i] = Math.round((confidence[i]/maxConfidence) * 100);
			$('#ratings').append('<span class="email" id="email' + i.toString() + '" >' + confidence[i].toString() + '</span>');
		}

		for (var i = 0; i < emails.length; i++) {
			$('#email' + i.toString()).barIndicator({
				forceAnim: true,
				horTitle: emails[i],
				horBarHeight:20,
				horLabelPos: 'topRight',
				labelVisibility: 'hidden',
				milestones: {},
				colorRange: true,
				colorRangeLimits: {
					optimal: '95-100-4AA64F',
					newRangeOne: '85-100-#B1DC44',
					newRangeTwo: '50-85-#F8D849',
					newRangeThree: '25-50-#FFBD5C',
					critical: '0-25-#FF3333'
				}
			});
		}
	}
}