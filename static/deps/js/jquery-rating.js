$(document).ready(function() {
  $(".star-container").on("click", ".star", function() {
    const rating = $(this).data("rating");
    const product_id = $(this).closest(".star-container").data("product-id");

    function updateUI(average_rating) {
      $('.star-container').find('.star').each(function(index) {
        const isFilled = index < average_rating;
        $(this).toggleClass('star-filled', isFilled).toggleClass('star-empty', !isFilled);
      });
    }

    $.ajax({
      url: `/catalog/add-rating/${product_id}/`,
      method: 'POST',
      data: {
        rating: rating,
        csrfmiddlewaretoken: '{{ csrf_token }}'
      },
      success: function(response) {
        if (response.success) {
          updateUI(response.average_rating);
          console.log('Average Rating:', response.average_rating);
        } else {
          console.error('Error:', response.error);
        }
      },
      error: function(xhr, errmsg, err) {
        console.error('AJAX Error:', errmsg);
      }
    });
  });
});
