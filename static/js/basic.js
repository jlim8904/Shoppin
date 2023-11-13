$(document).ready(function (){
    $("form").keypress(function(e) {
        //Enter key
        if (e.which == 13) {
            return false;
        }
    });
});


function plus(amountId) {
    let amount = parseInt($('#' + amountId).val())
    amount += 1
    $('#' + amountId).val(amount)
}

function minus(amountId) {
    let amount = parseInt($('#' + amountId).val())
    if (amount > 0){
        amount -= 1
        $('#' + amountId).val(amount)
    }
}

function plusCart(amountId) {
    let amount = parseInt($('#' + amountId + '_amount').val())
    amount += 1
    $('#' + amountId + '_amount').val(amount)
    count(amountId)
}

function minusCart(amountId) {
    let amount = parseInt($('#' + amountId + '_amount').val())
    if (amount > 0){
        amount -= 1
        $('#' + amountId + '_amount').val(amount)
    }
    count(amountId)
}


function count(id){
    let price = parseInt($('#' + id + '_price').text())
    let quantity = $('#' + id + '_amount').val()
    console.log(price)
    console.log(quantity)
    $('#' + id + '_total_price').val(''+(price * quantity))
}



function changeActive(btnId) {
    $('#' + btnId).attr('disabled', false)
}

function checkPassword() {
    let newPassword = $('#inputnewpassword3').val()
    let checkPassword = $('#inputconfirmpassword3').val()

    if (newPassword != checkPassword){
        $('#savePassword').attr('disabled', true)
        $('#warning').text('新密碼輸入錯誤')
        return false
    }else{
        $('#warning').empty()
        $('#savePassword').attr('disabled', false)
    }
}

function manuallyProcess(orderId) {
    let progress_bar = $('#' + orderId + ' .progress-bar')
    let percent = parseInt($('#' + orderId + ' .progress-bar').attr('aria-valuenow'))
    if (percent < 100){
        percent += 25
        let str_percent = '' + percent
        progress_bar.attr('aria-valuenow', str_percent)
        progress_bar.css('width', str_percent + '%')

        if (percent == 100){
            $('#' + orderId + ' .finished-btn').attr('disabled', false)
        }
    }
}


function finishOrder(orderId) {
    $('#' + orderId).remove()
    
    let finished_order = '<div class="card my-3" id="' + orderId + '"><input class="card-header h5 border-0" value="訂單編號：' + orderId + '" disabled></input><div class="card-body"><h5 class="card-title">訂單內容</h5><div class="row"><div class="col-6 d-flex align-items-center justify-content-around my-1"><p id="' + orderId + 'productId1-1" class="card-text">Alex Homer, ASP.NET 2.0 Visual Web Developer 2005 x 2</p><button type="button" class="btn btn-outline-danger">退貨</button></div><div class="col-6 d-flex align-items-center justify-content-around my-1"><p id="' + orderId + 'productId1-2" class="card-text">CakePHP Application Development x 3</p><button type="button" class="btn btn-outline-danger">退貨</button></div></div></div></div>'

    $('#pills-finished').append(finished_order)
}