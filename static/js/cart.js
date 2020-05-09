var updateBtns = document.getElementsByClassName('update-cart');
var updateAddress = document.getElementsByClassName('js_change_shipping');

for (i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(e){
        var prodId = this.dataset.product;
        var action = this.dataset.action;

        if (user === 'AnonymousUser') {

        } else {
            updateUserCart(prodId, action);
        }
    });
}

for (i = 0; i < updateAddress.length; i++){
    updateAddress[i].addEventListener('click', function(e){
        var addressId = this.dataset.address_id;
        var type = this.dataset.address_type;

        if (user === 'AnonymousUser') {

        } else {
            updateOrderAddress(addressId, type);
        }
    });
}

function updateUserCart (product, action, qty=1) {
    var url = '/update_cart/';

    fetch(url, {
        method: 'POST',
        headers: {
            'content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'product': product, 'action': action, 'qty':qty})
    }).then((response) => {
        return response.json();
    }).then((data) => {
        location.reload();
    });
}

function updateOrderAddress (addressId, type) {
    var url = '/update_address/';

    fetch(url, {
        method: 'POST',
        headers: {
            'content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'addressId': addressId, 'type': type})
    }).then((response) => {
        return response.json();
    }).then((data) => {
        location.reload();
    });
}