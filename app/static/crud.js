function add_stock(){
    inputR = $('input[name="stockR"]:checked')
    inputCode = $('#inputCode')
    inputPrice = $('#inputPrice')
    alert(inputPrice.val())
    $.post("/add_stock", {
        market: inputR.val(),
        code: inputCode.val(),
        price: inputPrice.val()
    }).done(
        function(response){
            alert(response["text"])
            inputR.prop('checked', false);
            inputCode.val('');
            inputPrice.val('');
            $('#exampleModal').modal('toggle');
    }).fail(function() {
        alert('ragacas deendzra')
    })}

$('#deleteStocks').click(function() {
    var rame = $("div.show").prop('id');
    alert(rame);
})

$("#check-all").click(function () {
		if ($("input:checkbox").prop("checked")) {
			$("input:checkbox[name='row-check']").prop("checked", true);
		} else {
			$("input:checkbox[name='row-check']").prop("checked", false);
		}
	});