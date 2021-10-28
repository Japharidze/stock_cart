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

$("input[name='check-all'").click(function () {
		if ($(".active input:checkbox").prop("checked")) {
			$(".active input:checkbox[name='row-check']").prop("checked", true);
		} else {
			$(".active input:checkbox[name='row-check']").prop("checked", false);
		}
	});