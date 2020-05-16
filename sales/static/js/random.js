$(document).ready(function () {
    $('#existing_customer').select2({
        placeholder: "SELECT AN EXISTING CUSTOMER",
   });
});

$(function() {
  $('input[name="date"]').daterangepicker({
    singleDatePicker: true,
    showDropdowns: true,
    locale: {
        format: 'DD/MM/YYYY'
    },
    minYear: 2020,
    maxYear: parseInt(moment().format('YYYY'),10)
  }, function(start, end, label) {

  });
});

function changeExistingCust(sel) {
    url = '/sales/get-last-bal/'+sel.value
    $.get(url, function (data) {
        $('#last_balance').empty().append(data.current_bal)
        calculateTotalAmount()
    })
}

function calculateTotalAmount(){
    let total_amount = 0

    let sub_total = parseFloat($('#sub_total').val())
    sub_total = isNaN(sub_total) ? 0 : sub_total

    let last_balance = parseFloat($('#last_balance').text())
    last_balance = isNaN(last_balance)? 0 : last_balance

    let pf = parseFloat($('#p_and_f').val())
    pf = isNaN(pf)? 0 : pf

    total_amount = sub_total + last_balance + pf
    $('#total_amount').empty().append(total_amount.toFixed(2))
}

function saveRandomBill() {
    let url = '/sales/random-bill/'
    let form = $('<form action='+ url +' method="POST"></form>');

    let csrfmiddlewaretoken = $('<input name = "csrfmiddlewaretoken" type="hidden"></input>');
    csrfmiddlewaretoken.val($("input[name='csrfmiddlewaretoken']").val());

    let form_customer = $('<input name = "customer" type="hidden"></input>')
    let form_date = $('<input name = "date" type="hidden"></input>')
    let form_last_bal = $('<input name = "last_balance" type="hidden"></input>')
    let form_sub_total = $('<input name = "sub_total" type="hidden"></input>')
    let form_p_and_f = $('<input name = "p_and_f" type="hidden"></input>')
    let form_total_amount = $('<input name = "total_amount" type="hidden"></input>')
    let form_amount_paid = $('<input name = "amount_paid" type="hidden"></input>')

    form_customer.val($('#existing_customer').val())
    form_date.val($('#date').val())

    let last_balance = parseFloat($('#last_balance').text())
    last_balance = isNaN(last_balance)? 0 : date
    form_last_bal.val(last_balance)

    let sub_total = parseFloat($('#sub_total').val())
    sub_total = isNaN(sub_total)? 0 : sub_total
    form_sub_total.val(sub_total)

    let p_and_f = parseFloat($('#p_and_f').val())
    p_and_f = isNaN(p_and_f)? 0 : p_and_f
    form_p_and_f.val(p_and_f)

    let total_amount = parseFloat($('#total_amount').text())
    total_amount = isNaN(total_amount)? 0 : total_amount
    form_total_amount.val(total_amount)

    let amount_paid = parseFloat($('#amount_paid').text())
    amount_paid = isNaN(amount_paid)? 0 : amount_paid
    form_amount_paid.val(amount_paid)

    form.append(csrfmiddlewaretoken, form_customer, form_date)
    form.append(form_last_bal, form_sub_total, form_p_and_f)
    form.append(form_total_amount, form_amount_paid)

    $('body').append(form);
    form.submit();
}