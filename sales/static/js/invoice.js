function generateTable(i){
    $('#tbody').append("<tr id='tr_item_"+i+"'>"+
        "<td class='text-center' style='padding-top:15px;'>"+i+"</td>"+
        "<td><input class='form-control' type='text' id='item_name_"+i+"'></td>"+
        "<td><input class='form-control' type='number' value=1 id='item_quantity_"+i+"' value onchange='calculate_row_total(this.id)'></td>"+
        "<td><input class='form-control' type='number' id='item_mrp_"+i+"' value onchange='calculate_row_total(this.id)'></td>"+
        "<td><input class='form-control' type='number' id='item_discount_"+i+"' value onchange='calculate_row_total(this.id)'></td>"+
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
    let remaining_balance = total_amount - parseFloat($('#amount_paid').val());
    $('#remaining_balance').empty().append(remaining_balance)
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
            "                    <input type='text' name='name' class='form-control' placeholder='Name of Customer...'>\n" +
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
            "                    <input type='text' name=\"address\" class='form-control' placeholder='Address...'>\n" +
            "                  </div>\n" +
            "                  <label for='phone' class='col-sm-1 control-label'>Phone</label>\n" +
            "                  <div class='col-sm-2'>\n" +
            "                    <input type='number' name='primary_num' class='form-control' placeholder='Phone Number'>\n" +
            "                  </div>\n" +
            "              </div>"
        )
    }
}

function saveInvoice() {
    let items_count = parseInt($('#tbody tr').length);
    let product_list = [];
    let final_summary = [];
    for(let i=1; i <= items_count; i++){
        if($('#item_total_'+i).text() !== ''){
            product_list.push({
                'product': $('#item_name_'+i).val(),
                'quantity': parseFloat($('#item_quantity_'+i).val()),
                'mrp': parseFloat($('#item_mrp_'+i).val()),
                'discount': parseFloat($('#item_discount_'+i).val()),
                'total': parseFloat($('#item_total_'+i).text()),
            });
        }
    }
    final_summary.push({
        'sub_total': parseFloat($('#sub_total').text()),
        'last_balance': parseFloat($('#last_balance').val()),
        'p_and_f': parseFloat($('#p_and_f').val()),
        'round_off': parseFloat($('#round_off').val()),
        'amount_paid': parseFloat($('#amount_paid').val()),
        'total_amount': parseFloat($('#total_amount').text()),
        'remaining_balance': parseFloat($('#remaining_balance').text()),
        'payment_mode': $('#payment_mode').val(),
    });

    // TODO: Make AJAX call to server...
}