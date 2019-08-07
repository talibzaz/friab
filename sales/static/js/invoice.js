function createItemsTable() {
            //$('#tbody').empty();
            let rowCount = parseInt($('#tbody tr').length);
            let items_count = $('#total_items').val();
            if(rowCount === 0){
                for(let i=1; i<=items_count; i++){
                    $('#tbody').append("<tr id='tr_item_"+i+"'>"+
                        "<td>"+i+"</td>"+
                        "<td><input class='form-control' type='text' id='item_name_"+i+"'></td>"+
                        "<td><input class='form-control' type='number' value=1 id='item_quantity_"+i+"' value onchange='calculate_total(this.id)'></td>"+
                        "<td><input class='form-control' type='number' id='item_mrp_"+i+"' value onchange='calculate_total(this.id)'></td>"+
                        "<td><input class='form-control' type='number' id='item_discount_"+i+"' value onchange='calculate_total(this.id)'></td>"+
                        "<td class='text-center' style='padding-top:15px'><b><span id='item_total_"+i+"'></span></b></td>"+
                        "<td class='text-center'>" +
                            "<a class='btn' id="+i+" onclick='clearRowData(this.id)'><i class='fa fa-clear'></i>x</a>" +
                        "</td>"+
                        "</tr>"
                    );
                }
            } else {
                for(let i=rowCount+1; i <= rowCount+parseInt(items_count); i++){
                    $('#tbody').append("<tr id='tr_item_"+i+"'>"+
                        "<td>"+i+"</td>"+
                        "<td><input class='form-control' type='text' id='item_name_"+i+"'></td>"+
                        "<td><input class='form-control' type='number' value=1 id='item_quantity_"+i+"' value onchange='calculate_total(this.id)'></td>"+
                        "<td><input class='form-control' type='number' id='item_mrp_"+i+"' value onchange='calculate_total(this.id)'></td>"+
                        "<td><input class='form-control' type='number' id='item_discount_"+i+"' value onchange='calculate_total(this.id)'></td>"+
                        "<td class='text-center' style='padding-top:15px'><b><span id='item_total_"+i+"'></span></b></td>"+
                        "<td class='text-center'>" +
                            "<a class='btn' id="+i+" onclick='clearRowData(this.id)'><i class='fa fa-clear'></i>x</a>" +
                        "</td>"+
                        "</tr>"
                    );
                }
            }

        }

function calculate_total(e){
    let res = e.split('_');

    let quantity = $('#item_quantity_'+res[2]).val();
    let mrp = $('#item_mrp_'+res[2]).val();
    let discount = $('#item_discount_'+res[2]).val();
    let total = (quantity * mrp) - ((quantity * mrp * discount) / 100);
    $('#item_total_'+res[2]).empty().append(total);

    let sub_total = 0;
    let items_count = parseInt($('#tbody tr').length);
    for(let i=1; i <= items_count; i++){
        let total = $('#item_total_'+i).text();
        if(total !== ''){
            sub_total += parseFloat(total)
        }
    }
    $('#sub_total').empty().append(sub_total);
    let total_amount = sub_total + parseFloat($('#last_balance').val()) + parseFloat($('#shipping_cost').val());
    $('#total_amount').empty().append(total_amount);
    let remaining_balance = total_amount - parseFloat($('#amount_paid').val());
    $('#remaining_balance').empty().append(remaining_balance)
}

function calculateGrandTotal() {
    let sub_total = parseFloat($('#sub_total').text());
    let total_amount = sub_total + parseFloat($('#last_balance').val()) + parseFloat($('#shipping_cost').val());
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
}

function customerChange() {
    let customer_type = $('#customer_type').val();
    if(customer_type === 'existing') {
        //MAKE AJAX CALL TO SERVER AND GET LIST OF CUSTOMERS
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
            "                  <label for='date' class='col-sm-1 control-label'>Date</label>\n" +
            "                  <div class='col-sm-2'>\n" +
            "                    <input type='date' name='date' class='form-control' placeholder='Date'>\n" +
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

}