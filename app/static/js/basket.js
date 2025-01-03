// this script is responsible for implementing AJAX for the basket
// to increase/ decrease basket item quantities without reloading the page

$(document).ready(function () {
    $(".update-basket").click(function (e) {
        e.preventDefault();
        const itemId = $(this).data("item-id");
        const action = $(this).data("action");
        // ajax post request
        $.ajax({
            url: "/update_basket",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                item_id: itemId,
                action: action,
            }),
            headers: {
                "X-CSRFToken": $("input[name=csrf_token]").val(),
            },
            success: function (data) {
                if (data.success) {
                    // Update quantity and totals dynamically
                    $(`#item-quantity-${itemId}`).text(data.quantity);
                    $(`#item-total-${itemId}`).text(`£${data.item_total.toFixed(2)}`);
                    $("#basket-total").text(`Total: £${data.basket_total.toFixed(2)}`);
                    // Remove item row if quantity is zero
                    if (data.quantity === 0) {
                        $(`#basket-item-${itemId}`).remove();
                    }
                } else {
                    alert(data.message || "Error updating the basket.");
                }
            },
            error: function (xhr, status, error) {
                console.error("Error:", error);
            },
        });
    });
});
