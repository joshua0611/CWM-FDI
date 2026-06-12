document.addEventListener("DOMContentLoaded", function () {
    function calculateTotalPrice() {
        let total = 0;
        document.querySelectorAll(".generic-price").forEach(function (priceElement) {
            let priceText = priceElement.textContent.trim().replace("€", ""); // Remove € sign
            let price = parseFloat(priceText);
            if (!isNaN(price)) {
                total += price;
            }
        });

        // Update the total price display
        let totalPriceElement = document.querySelector(".total-price");
        if (totalPriceElement) {
            totalPriceElement.textContent = `Total Price: €${total.toFixed(2)}`;
        }
    }

    calculateTotalPrice();
});