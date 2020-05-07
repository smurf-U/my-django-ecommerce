var updateBtns = document.getElementsByClassName('update-cart');

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