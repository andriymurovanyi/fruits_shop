$(document).ready(() => {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                const csrfToken = getCookie('csrftoken')
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }
        }
    });

    getCartDetails();
});


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

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function setCartCount(cartId, count) {
    const cartCount = $(cartId);
    const cartCountText = count > 9 ? '9+' : count;

    cartCount.text(cartCountText);
}

function getCartDetails() {
    $.ajax({
        url: '/cart/all',
        type: 'get',
        dataType: 'json',
        success: (response) => {
            if (response && response.status === 200) {
                const { cart_length: count } = response;
                setCartCount('#lblCartCount', parseInt(count));
            }
        }
    })
}

function addProductToCart(event, productId, quantity = 1) {
    $.ajax({
        url: `/cart/add/${productId}`,
        type: 'post',
        data: {
            quantity
        },
        success: (response) => {
            if (response && response.status === 200) {
                const {cart_length: count} = response;

                const loadingText = '<i class="fa fa-circle-o-notch fa-spin"></i>';

                const activeBtn = $(`#btn_${productId}`);

                if (activeBtn.html() !== loadingText) {
                    activeBtn.data('original-text', activeBtn.html());
                    activeBtn.html(loadingText);
                }

                setTimeout(function () {
                    activeBtn.html(activeBtn.data('original-text'));
                    setCartCount('#lblCartCount', parseInt(count));
                }, 500);
            }
        }
    });

    return false;
}

function buyProduct(productId, quantity = 1) {
    $.ajax({
        url: `/cart/add/${productId}`,
        type: 'post',
        data: {
            quantity,
            single_buy: 'yes'
        },
        success: () => {
            window.location.replace('/cart')
        }
    });
}

function removeProductFromCart(productId) {
    $.ajax({
        url: `/cart/remove/${productId}`,
        type: 'post',
        success: (response) => {
            if (response) {
                const {
                    cart_length: count,
                    total_price
                } = response;

                if (parseInt(total_price) <= 0) {
                    window.location.reload();
                }

                const productRow = $(`#product_${productId}`);
                const totalPriceSection = $('#total_price');

                totalPriceSection.html(`Итого: ${total_price} грн.`);
                productRow.remove();

                setCartCount('#lblCartCount', parseInt(count));
            }
        }
    });

    return false;
}