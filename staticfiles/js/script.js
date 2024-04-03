$("#menu-button").on("click", function () {
  $("#icon").toggleClass("hidden");
  $("#close-icon").toggleClass("hidden");
  $("#nav-links").toggleClass("-translate-y-full opacity-100");
});

// add
$('#add-button').on("click", function (e) {
  e.preventDefault();
  $.ajax({
    type: 'POST',
    url: '{% url "orders:product_add" %}',
    data: {
      product_id: $('#add-button').val(),
      csrfmiddlewaretoken: "{{csrf_token}}",
      action: 'post'
    },
    success: function (json) {
      document.getElementById("cart-quantity").innerHTML = json.quantity
      document.getElementById("subtotal").innerHTML = json.subtotal;
    },
    error: function (xhr, errmsg, err) { }
  });
});

// delete
$('#remove-button').on("click", function (e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: '{% url "orders:cart_delete" %}',
    data: {
      product_id: $(this).data("index"),
      csrfmiddlewaretoken: "{{csrf_token}}",
      action: "post",
    },
    success: function (json) {
      $('#' + cart_id).remove();
      if (json.quantity == 0) {
        subtotal = 0
      } else {
        subtotal = json.subtotal
      }
      $("#cart-quantity").replaceWith(json.quantity);
      $("#subtotal").replaceWith(json.subtotal);
    },
    error: function (xhr, errmsg, err) { },
  });
});



// clear
$("#clear-button").on("click", function (e) {
  e.preventDefault();
  $.ajax({
    url: '{%url "orders: cart_clear"%}',
    type: 'GET',
    success: function (json) {
      $('.cart-item').remove();

      $("#cart-quantity").replaceWith(json.quantity);
      $("#subtotal").replaceWith(json.subtotal);
    },
    error: function (xhr, errmsg, err) { },
  });
});