var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
function ajaxDo(url, type, data, callback) {
	$.ajax({
		url: url,
		type: type,
		headers: {
			'X-CSRFToken': csrftoken
		},
		data: data
	}).done(function(response) {
		callback(response);
	});
}
