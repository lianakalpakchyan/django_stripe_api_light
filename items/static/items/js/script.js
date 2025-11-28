function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function makeOrderCode(length) {
    let result = '';
    let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let charactersLength = characters.length;
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

function calculateTotalPrice(subTotal, order) {
    let discount = order.discount == null ? 0 : order.discount.percent_off;
    let totalPrice = subTotal * (100 - discount) / 100;
    if(order.tax && order.tax.inclusive == false){
        totalPrice = totalPrice * (1 + order.tax.percentage / 100);
    }
    return totalPrice.toFixed(2);
}

function hideOrder() {
    $('.order-items').html('<hr>No item is chosen yet...');
    $('.order-summary').hide();
}

// -----------------------------------------------

function getDiscountList(){
    fetch('/discount_list', { method: 'GET' })
    .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        fillDiscount(data);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

function getTaxList(){
    fetch('/tax_list', { method: 'GET' })
    .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        fillTax(data);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

function getOrderItems(){
    fetch('/order', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Order-Code': orderCode
        },
    })
    .then(response => {
        if (!response.ok) {
          hideOrder()
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        return fillOrder(data);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

// -----------------------------------------------

function fillDiscount(discountList) {
    for(let i = 0; i < discountList.length; i++){
        $('#discount').append(`
            <option value="${discountList[i].id}">${discountList[i].percent_off}%</option>
        `);
    }
}

function fillTax(taxList) {
    for(let i = 0; i < taxList.length; i++){
        $('#tax').append(`
            <option value="${taxList[i].id}">${taxList[i].display_name} - ${taxList[i].percentage}%</option>
        `);
    }
}

function fillOrder(order) {
    let orderItems = order.orderitems;
    $('.order-items').html('');

    if(orderItems.length > 0){
        for(let i = orderItems.length - 1; i > -1; i--){
            $('.order-items').append(`
                <div class="order-item d-flex justify-content-between">
                    <input type="hidden" class="orderItemId" value="${orderItems[i].id}">
                    <div>
                        <h5>${orderItems[i].item.name}</h5>
                        <input type="number" class="form-control w-50 update" value="${orderItems[i].quantity}" min="1">
                    </div>
                    <div class="d-flex flex-column justify-content-between">
                        <span>${orderItems[i].item.currency} ${orderItems[i].sub_total}</span>
                        <button class="btn btn-sm btn-danger remove">Remove</button>
                    </div>
                </div>
            `);
        }
        $('.order-summary').show();
        fillOrderSummary(order, orderItems);
    }
    else{
        hideOrder();
    }

}

function fillOrderSummary(order, orderItems) {
    let currency = orderItems[0].item.currency;
    $('#subtotal').text(order.order_total.toFixed(2));
    $('#subtotal-cur').text(currency);
    if(order.tax != null){
        $('#tax').val(order.tax.id);
    }
    if(order.discount != null){
        $('#discount').val(order.discount.id);
    }
    let totalPrice = calculateTotalPrice($('#subtotal').text(), order);
    $('#total-price').text(totalPrice);
    $('#total-price-cur').text(currency);
}


// -----------------------------------------------

function addItemToOrder() {
    if(orderCode == null){
        orderCode = makeOrderCode(11);
        localStorage.setItem("order_code", orderCode);
    }

    fetch('/order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Order-Code': orderCode
        },
        body: JSON.stringify({item_id: $(this).siblings('.itemId').val()}),
    })
    .then(response => response.json())
    .then(data => {
        if( data.error ){
            alert(data.error);
        }
        else{
            fillOrder(data);
        }
    })
}

function updateOrder(updateValue) {
    fetch('/order', {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Order-Code': orderCode
        },
        body: JSON.stringify(updateValue)
    })
    .then(response => response.json())
    .then((data) => {
        let totalPrice = calculateTotalPrice($('#subtotal').text(), data);
        $('#total-price').text(totalPrice);
    });
}

// -----------------------------------------------

function setUpOrder(){
    getDiscountList();
    getTaxList();
    if(orderCode){
        getOrderItems();
    }
    else{
        hideOrder();
    }
}

let orderCode = localStorage.getItem("order_code");
const csrftoken = getCookie('csrftoken');
