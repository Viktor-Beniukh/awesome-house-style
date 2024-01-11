$(document).ready(function() {
    $(document).on('click', '.favorite-icon', function(event) {
        event.preventDefault();

        const icon = $(this);
        const product_id = icon.data('product-id');

        $.ajax({
            url: '/catalog/toggle-favorite/',
            type: 'POST',
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(response) {
                if (response.is_favorite) {
                    icon.addClass('favorite');
                } else {
                    icon.removeClass('favorite');

                    icon.closest('.card-product').remove();

                    if ($('.card-product').length === 0) {
                        $('#no-products-msg').show();
                    }
                }

                $('.favorites-count').text(response.favorites_count);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
