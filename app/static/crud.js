$('#deleteStocks').click(function() {
    var checked_boxes = $('input[name="row-check"]:checked')
    var list = checked_boxes.map(function() {
        return this['value'];
    }).get();
    $.post("/delete_stocks", {"ids": list.join(',')}).done(
        function(){
            location.reload();
        });
})

$("#check-all").click(function () {
		if ($("input:checkbox").prop("checked")) {
			$("input:checkbox[name='row-check']").prop("checked", true);
		} else {
			$("input:checkbox[name='row-check']").prop("checked", false);
		}
	});