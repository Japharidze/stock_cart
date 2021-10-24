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