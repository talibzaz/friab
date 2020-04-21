$(document).ready(function () {
    $('.date').hide();
    $('.ctnr').hide();
});

function field_type(){
    let val = $('#criteria').val();
    if(val === 'date'){
        $('.name').hide();
        $('.date').show();
        $('#date_value').focus();
    } else {
        $('.date').hide();
        $('.name').show();
        $('#input_value').focus();
        $('#input_value').select();
    }
}

$('#input_value').keypress(function (e) {
    if (e.keyCode === 13){
        $('.btn').click();
    }
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

function getInvoiceData() {
    $('#tbody').empty();
    let criteria = $('#criteria').val();
    let input_value = $('#input_value').val();
    if (criteria === 'date'){
        input_value = $('#date_value').val()
    }
    if(criteria === "0" || input_value === ''){
        alert('TRY AGAIN');
        return
    }

    $.post('/sales/search-invoice/', {
        'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
        'criteria': criteria,
        'value': input_value
    }, function (data) {
        if(typeof data['error'] !== 'undefined') {
            $('.ctnr').hide();
            alert('Try Again');
            return
        }
        let json = JSON.parse(data);
        for (i in json){
            $('#tbody').append("<tr>\n" +
                "                  <td>"+json[i].customer_name+"</td>\n" +
                "                  <td>"+json[i].id+"</td>\n" +
                "                  <td>"+json[i].date+"</td>\n" +
                "                  <td>"+json[i].total_amount+"</td>\n" +
                "                  <td style='text-align: center'>" +
                "<a href='/sales/update-invoice/"+ json[i].id +"' class='btn btn-primary btn-get'>Get</a>" +
                "                  </td>\n" +
                "                </tr>")
        }
        $('.ctnr').show()
    });
}

$('body').on('click', '.btn-get', function () {
    console.log(this.id);
});