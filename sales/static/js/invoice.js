// RELOAD PAGE EVERYTIME BACK BUTTON GETS PRESSED ON BROWSER.
$(document).ready(function () {
    if(!!window.performance && window.performance.navigation.type === 2)
    {
        window.location.reload();
    }
   document.getElementById("name").focus()

});

// EVENTS TRIGGERED ON PRESSING ENTER.
$('body').on('keypress', 'input', function (e) {
    if (e.which === 13) {
       e.preventDefault();
       let inputs = $(':input');
       let nextInput = inputs.get(inputs.index(this) + 1);
       if (nextInput) {
          nextInput.focus();
          nextInput.select();
       }
    }
});

// THIS FUNCTION CREATES TABLE.
function generateTable(i){
    $('#tbody').append("<tr id='tr_item_"+i+"'>"+
        "<td class='text-center' style='padding-top:15px;' id='serial_"+i+"'>"+i+"</td>"+
        "<td><input class='form-control body_ele' type='text' id='item_name_"+i+"'></td>"+
        "<td><input class='form-control body_ele' type='number' id='item_mrp_"+i+"' onkeyup='calculate_row_total(this.id)''></td>"+
        "<td><input class='form-control body_ele' type='number' value=1 id='item_quantity_"+i+"' onkeyup='calculate_row_total(this.id)'></td>"+
        "<td><input class='form-control body_ele' type='number' id='item_discount_"+i+"' onkeyup='calculate_row_total(this.id)'></td>"+
        "<td class='text-center' style='padding-top:15px'><b><span id='item_total_"+i+"'></span></b></td>"+
        "<td class='text-center'>" +
            "<a class='btn' id="+i+" onclick='clearRowData(this.id)'><i class='fa fa-clear'></i>x</a>" +
        "</td>"+
        "</tr>"
    );
}

// THIS FUNCTION CREATES TABLE BASED ON USER'S INPUT FOR NUMBER OF ROWS IN TABLE
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

// ADDS ONLY ONE ROW IN THE TABLE.
function addOneRow() {
    let rowCount = parseInt($('#tbody tr').length);
    if (rowCount === 0){
        generateTable(1);
        document.getElementById("item_name_"+1).focus()
    } else {
        let current_row = rowCount + 1;
        generateTable(rowCount+1);
        document.getElementById("item_name_"+current_row).focus()
    }
}

// CALCULATES THE SUB TOTAL OF BILL.
function calculateSubTotal() {
    let sub_total = 0;
    let items_count = parseInt($('#tbody tr').length);
    for(let i=1; i <= items_count; i++){
        let total = $('#item_total_'+i).text();
        if(total !== ''){
            sub_total += parseFloat(total)
        }
    }
    $('#sub_total').empty().append(sub_total.toFixed(2));
    calculateGrandTotal();
}

// CALCULATES THE TOTAL AMOUNT OF JUST ONE ROW.
function calculate_row_total(e){
    let res = e.split('_');

    let quantity = $('#item_quantity_'+res[2]).val();
    let mrp = $('#item_mrp_'+res[2]).val();
    let discount = $('#item_discount_'+res[2]).val();
    let total = (quantity * mrp) - ((quantity * mrp * discount) / 100);
    $('#item_total_'+res[2]).empty().append(total.toFixed(2));

    calculateSubTotal();
}

// CALCULATES THE GRAND TOTAL OF BILL
function calculateGrandTotal() {
    let total_amount = parseFloat($('#sub_total').text()) + parseFloat($('#last_balance').val()) +
        parseFloat($('#p_and_f').val()) + parseFloat($('#round_off').val()) ;
    $('#total_amount').empty().append(total_amount.toFixed(2));
    let current_balance = total_amount - parseFloat($('#amount_paid').val());
    $('#current_balance').empty().append(current_balance.toFixed(2))
}

// CLEARS THE DATA IN ONE SINGLE ROW
function clearRowData(id) {
    $('#item_name_'+id).val('');
    $('#item_quantity_'+id).val(1);
    $('#item_mrp_'+id).val('');
    $('#item_discount_'+id).val('');
    $('#item_total_'+id).text('');
    $('#round_off').val(0);
    calculateSubTotal();
}

function clearReturnData(id) {

}
function addOneReturnRow() {

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

//THE COMMON CODE BETWEEN CREATE INVOICE AND UPDATE INVOICE
function commonStuff(url, update=false, invoice_id=null) {
let items_count = parseInt($('#tbody tr').length);
    let product_list = {};
    let final_summary = {};
    let counter = 0;

    for(let i=1; i <= items_count; i++){
        if($('#item_total_'+i).text() !== ''){
            counter++;
            let mrp =0, discount_amount=0, price = 0;
            let discount_percent=parseFloat($('#item_discount_'+i).val());
            let quantity = parseFloat($('#item_quantity_'+i).val())
            let product = $('#item_name_'+i).val().toUpperCase()
            mrp = parseFloat($('#item_mrp_'+i).val());


            let validity = form_validity_check(product, quantity, discount_percent, mrp);
            if (!validity){
                return
            }
            if(isNaN(discount_percent)){
                discount_percent = 0;
            }

            discount_amount = mrp * discount_percent/100;
            price = mrp - discount_amount;
            if (update){
                product_list[i] = {
                'serial': counter,
                'item_id': $('#item_id_'+i).length !== 0 ? $('#item_id_'+i).val() : 0,
                'product': product,
                'mrp': mrp,
                'discount': discount_percent,
                'quantity': quantity,
                'price': price.toFixed(2),
                'total': parseFloat($('#item_total_'+i).text()),
                }
            } else {
                product_list[i] = {
                'serial': counter,
                'product': product,
                'mrp': mrp,
                'discount': discount_percent,
                'quantity': quantity,
                'price': price.toFixed(2),
                'total': parseFloat($('#item_total_'+i).text()),
                }
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
    final_summary['balance_bill'] = $('#balance_bill').is(":checked")

    let form = $('<form action='+ url +' method="POST"></form>');
    let csrfmiddlewaretoken = $('<input name = "csrfmiddlewaretoken" type="hidden"></input>');
    let customer_name = $('<input name = "cus_name" type="hidden"></input>');
    let customer_address = $('<input name = "cus_address" type="hidden"></input>');
    let customer_phone = $('<input name = "cus_phone" type="hidden"></input>');
    let item_list = $('<input name = "product_list" type="hidden"></input>');
    let summary = $('<input name = "final_summary" type="hidden"></input>');

    csrfmiddlewaretoken.val($("input[name='csrfmiddlewaretoken']").val());
    customer_name.val($('#name').val() !== ''? $('#name').val().toUpperCase() : 'CASH');
    customer_address.val($('#address').val().toUpperCase());
    customer_phone.val($('#phone').val());
    item_list.val(JSON.stringify(product_list));
    summary.val(JSON.stringify(final_summary));
    if (update){
        let inv_id = $('<input name = "invoice_id" type="hidden"></input>');
        inv_id.val(invoice_id);
        form.append(inv_id);
    }
    form.append(csrfmiddlewaretoken, customer_name);
    form.append(customer_address, customer_phone);
    form.append(item_list, summary);
    $('body').append(form);
    form.submit();
}

// SENDS THE FINAL DATA TO SERVER FOR PDF GENERATION PURPOSE.
function saveInvoice() {
    let url = "/sales/billing/sale-bill/";
    commonStuff(url)
}

// UPDATES THE INVOICE IN DB.
function updateInvoice(invoice_id) {
    let url = "/sales/update-invoice/";
    let update = true;
    commonStuff(url, update, invoice_id)
}

function form_validity_check(product, quantity, discount_percent, mrp){
    if (product === ''){
        alert('Item name cannot be empty');
        return false
    }
    if (quantity < 1) {
        alert('Quantity cannot be less than 1');
        return false
    }
    if(isNaN(mrp) || mrp < 1){
        alert('Mrp cannot be less than 1');
        return false
    }
    if (discount_percent < 0){
        alert('Discount cannot be less than 1');
        return false
    }
    return true
}