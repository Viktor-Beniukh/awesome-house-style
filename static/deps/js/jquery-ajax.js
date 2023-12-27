$(document).ready(function () {
    const successMessage = $("#jq-notification");

    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();

        const goodsInCartCount = $("#goods-in-cart-count");
        let cartCount = parseInt(goodsInCartCount.text() || 0);

        const product_id = $(this).data("product-id");

        const add_to_cart_url = $(this).attr("href");


        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);

                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                cartCount++;
                goodsInCartCount.text(cartCount);

                const cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Error adding of product to cart");
            },
        });
    });



    $(document).on("click", ".remove-from-cart", function (e) {
        e.preventDefault();

        const goodsInCartCount = $("#goods-in-cart-count");
        let cartCount = parseInt(goodsInCartCount.text() || 0);

        const cart_id = $(this).data("cart-id");

        const remove_from_cart = $(this).attr("href");


        $.ajax({

            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);

                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);

                const cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Error adding of product to cart");
            },
        });
    });



    $(document).on("click", ".decrement", function () {
        const url = $(this).data("cart-change-url");

        const cartID = $(this).data("cart-id");

        const $input = $(this).closest('.input-group').find('.number');

        const currentValue = parseInt($input.val());
        if (currentValue > 1) {
            $input.val(currentValue - 1);

            updateCart(cartID, currentValue - 1, -1, url);
        }
    });


    $(document).on("click", ".increment", function () {

        const url = $(this).data("cart-change-url");

        const cartID = $(this).data("cart-id");

        const $input = $(this).closest('.input-group').find('.number');

        const currentValue = parseInt($input.val());

        $input.val(currentValue + 1);


        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);

                setTimeout(function () {
                     successMessage.fadeOut(400);
                }, 7000);

                const goodsInCartCount = $("#goods-in-cart-count");
                let cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                const cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Error adding of product to cart");
            },
        });
    }

});