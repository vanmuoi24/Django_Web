var update = document.getElementsByClassName("update-cart");
for (let i = 0; i < update.length; i++) {
  update[i].addEventListener("click", (event) => {
    var productId = event.target.dataset.product;
    var action = event.target.dataset.action;

    if (user === "AnonymousUser") {
      console.log("user not login");
    } else {
      updateUserOrder(productId, action);
      alert("Thêm Sản Phẩm Thành Công");
      location.reload();
    }
  });
}
function updateUserOrder(productId, action, quantity) {
  console.log("user login ");
  var url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json", // Đã sửa
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      productId: productId,
      action: action,
      quantity: quantity,
    }), // Gửi số lượng mới
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data", data);
      // Cập nhật lại tổng giá của giỏ hàng nếu cần
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const quantityInputs = document.querySelectorAll(".quantity-input");

  quantityInputs.forEach(function (input) {
    input.addEventListener("change", function () {
      const productId = input.getAttribute("data-product-id");
      const quantity = parseInt(input.value); // Chuyển đổi giá trị nhập vào thành số nguyên
      const price = parseFloat(input.getAttribute("data-price"));
      location.reload();
      if (!isNaN(quantity) && quantity > 0 && !isNaN(price)) {
        const totalPrice = quantity * price; // Tính tổng giá
        document.getElementById(`total-price-${productId}`).textContent =
          totalPrice.toLocaleString("vi-VN") + "₫";
        updateUserOrder(productId, "update", quantity);
        location.reload();
      } else {
        document.getElementById(`total-price-${productId}`).textContent = "0₫";
        location.reload();
      }
    });
  });
});
