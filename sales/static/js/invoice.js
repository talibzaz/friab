function generateTable(i){
    $('#tbody').append("<tr id='tr_item_"+i+"'>"+
        "<td class='text-center' style='padding-top:15px;' id='serial_"+i+"'>"+i+"</td>"+
        "<td><input class='form-control' type='text' id='item_name_"+i+"'></td>"+
        "<td><input class='form-control' type='number' value=1 id='item_quantity_"+i+"' onkeyup='calculate_row_total(this.id)'></td>"+
        "<td><input class='form-control' type='number' id='item_mrp_"+i+"' onkeyup='calculate_row_total(this.id)''></td>"+
        "<td><input class='form-control' type='number' id='item_discount_"+i+"' onkeyup='calculate_row_total(this.id)'></td>"+
        "<td class='text-center' style='padding-top:15px'><b><span id='item_total_"+i+"'></span></b></td>"+
        "<td class='text-center'>" +
            "<a class='btn' id="+i+" onclick='clearRowData(this.id)'><i class='fa fa-clear'></i>x</a>" +
        "</td>"+
        "</tr>"
    );
}

function addMultipleRows() {
    let rowCount = parseInt($('#tbody tr').length);
    let items_count = parseInt($('#total_items').val());
    if(rowCount === 0){
        for(let i=1; i<=items_count; i++){
            generateTable(i)
        }
    } else {
        for(let i=rowCount+1; i <= rowCount+items_count; i++){
            generateTable(i)
        }
    }
}

function addOneRow() {
    let rowCount = parseInt($('#tbody tr').length);
    if (rowCount === 0){
        generateTable(1)
    } else {
        generateTable(rowCount+1)
    }
}

function calculateSubTotal() {
    let sub_total = 0;
    let items_count = parseInt($('#tbody tr').length);
    for(let i=1; i <= items_count; i++){
        let total = $('#item_total_'+i).text();
        if(total !== ''){
            sub_total += parseFloat(total)
        }
    }
    $('#sub_total').empty().append(sub_total);
    calculateGrandTotal();
}

function calculate_row_total(e){
    let res = e.split('_');

    let quantity = $('#item_quantity_'+res[2]).val();
    let mrp = $('#item_mrp_'+res[2]).val();
    let discount = $('#item_discount_'+res[2]).val();
    let total = (quantity * mrp) - ((quantity * mrp * discount) / 100);
    $('#item_total_'+res[2]).empty().append(total);

    calculateSubTotal();
}

function calculateGrandTotal() {
    let total_amount = parseFloat($('#sub_total').text()) + parseFloat($('#last_balance').val()) +
        parseFloat($('#p_and_f').val()) + parseFloat($('#round_off').val()) ;
    $('#total_amount').empty().append(total_amount);
    let current_balance = total_amount - parseFloat($('#amount_paid').val());
    $('#current_balance').empty().append(current_balance)
}

function clearRowData(id) {
    $('#item_name_'+id).val('');
    $('#item_quantity_'+id).val(1);
    $('#item_mrp_'+id).val('');
    $('#item_discount_'+id).val('');
    $('#item_total_'+id).text('');
    $('#round_off').val(0);
    calculateSubTotal();
}

function customerChange() {
    let customer_type = $('#customer_type').val();
    if(customer_type === 'existing') {
        //TODO: MAKE AJAX CALL TO SERVER AND GET LIST OF CUSTOMERS
        let url = "{% url 'sales:customer-list' %}";

        $.get(url, function (data) {
            console.log(data)
        });
    }
    if(customer_type === 'retail'){
        $('#customer_details').empty().append(
            "<div class='row form-group'>\n" +
            "                  <label for='name' class='col-sm-2 control-label'>Name</label>\n" +
            "                  <div class='col-sm-4'>\n" +
            "                    <input type='text' id='name' class='form-control' placeholder='Name of Customer...'>\n" +
            "                  </div>\n" +
            "                  <label for='date' class='col-sm-1 control-label'>Category</label>\n" +
            "                  <div class='col-sm-2'>\n" +
            "                    <select id='category' class='form-control input-sm'>\n" +
            "                       <option value='cat_gen'>General</option> " +
            "                       <option value='cat_a'>Category A</option> " +
            "                       <option value='cat_b'>Category B</option> " +
            "                       <option value='cat_c'>Category C</option> " +
            "                    </select>\n" +
            "                  </div>\n" +
            "              </div>\n" +
            "              <div class='row form-group'>\n" +
            "                  <label for='address' class='col-sm-2 control-label'>Address</label>\n" +
            "                  <div class='col-sm-4'>\n" +
            "                    <input type='text' id='address' class='form-control' placeholder='Address...'>\n" +
            "                  </div>\n" +
            "                  <label for='phone' class='col-sm-1 control-label'>Phone</label>\n" +
            "                  <div class='col-sm-2'>\n" +
            "                    <input type='number' id='primary_num' class='form-control' placeholder='Phone Number'>\n" +
            "                  </div>\n" +
            "              </div>"
        )
    }
}

function saveInvoice() {
    let items_count = parseInt($('#tbody tr').length);
    let product_list = {};
    let final_summary = {};
    let counter = 0

    for(let i=1; i <= items_count; i++){
        if($('#item_total_'+i).text() !== '' && $('#item_name_'+i).val() !== ''){
            counter++;
            let mrp =0, discount=0, price = 0;
            mrp = parseFloat($('#item_mrp_'+i).val());
            discount = mrp * parseFloat($('#item_discount_'+i).val())/100;
            price = mrp - discount;
            product_list[i] = {
                'serial': counter,
                'product': $('#item_name_'+i).val().toUpperCase(),
                'quantity': parseFloat($('#item_quantity_'+i).val()),
                'price': price ,
                'total': parseFloat($('#item_total_'+i).text()),
            }
        }
    }
    final_summary['sub_total'] = parseFloat($('#sub_total').text());
    final_summary['last_balance'] = parseFloat($('#last_balance').val());
    final_summary['p_and_f'] = parseFloat($('#p_and_f').val());
    final_summary['round_off'] = parseFloat($('#round_off').val());
    final_summary['amount_paid'] = parseFloat($('#amount_paid').val());
    final_summary['total_amount'] = parseFloat($('#total_amount').text());
    final_summary['current_balance'] = parseFloat($('#current_balance').text());
    final_summary['payment_mode'] = $('#payment_mode').val();

    let form = $('<form action="/sales/billing/sale-bill/" method="POST"></form>');
    let csrfmiddlewaretoken = $('<input name = "csrfmiddlewaretoken" type="hidden"></input>');
    let customer_name = $('<input name = "cus_name" type="hidden"></input>');
    let customer_address = $('<input name = "cus_address" type="hidden"></input>');
    let customer_phone = $('<input name = "cus_phone" type="hidden"></input>');
    let item_list = $('<input name = "product_list" type="hidden"></input>');
    let summary = $('<input name = "final_summary" type="hidden"></input>');

    csrfmiddlewaretoken.val($("input[name='csrfmiddlewaretoken']").val());
    customer_name.val($('#name').val().toUpperCase());
    customer_address.val($('#address').val().toUpperCase());
    customer_phone.val($('#phone').val());
    item_list.val(JSON.stringify(product_list));
    summary.val(JSON.stringify(final_summary));

    form.append(csrfmiddlewaretoken, customer_name);
    form.append(customer_address, customer_phone);
    form.append(item_list, summary);

    $('body').append(form);
    form.submit();
    // $.post('/sales/billing/sale-bill/', {
    //     'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val(),
    //     'customer_name': $('#name').val(),
    //     'customer_address': $('#address').val(),
    //     'phone': $('#primary_num').val(),
    //     'product_list': JSON.stringify(product_list),
    //     'final_summary': JSON.stringify(final_summary),
    // }, function (data) {
    //     console.log(data)
    // })
    // let url = "/sales/billing/print-invoice/";
    // window.location.href = url
}