$(function() {
	var submit_form = function(e) {
		$('#calculate').removeClass('btn btn-default active').addClass('btn btn-success disabled');
		$('#calculate').text("Calculating...");
		$.getJSON("/calculate", {
			a: $('input[name="username"]').val()
			}, function(data) {
			if (data.count == undefined) { data.count = "0" };
			$("#result").text("This user's gh-index is: " + data.result + " They have " + data.count + " total stars.");
			$('#calculate').removeClass('btn btn-success disabled').addClass('btn btn-default active');
			$('#calculate').text("Calculate again");
		});
	};
	$('a#calculate').on('click', submit_form);
	$('#on_enter').keypress(function(e) {
		if (e.which == 13) {
			submit_form();
			return false;
			}
		});
});
