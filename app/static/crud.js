$('.deleteStocks').click(function() {
    var checked_boxes = $('.show input[name="row-check"]:checked')
    var list = checked_boxes.map(function() {
        return this['value'];
    }).get();
    if (list.length == 0){
        return
    };
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