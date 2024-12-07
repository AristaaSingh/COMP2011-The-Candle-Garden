document.addEventListener("DOMContentLoaded", function () {
    const newAddressFields = document.getElementById("new-address-fields");
    const addressInputs = document.querySelectorAll('input[name="delivery_address_id"]');
    const addressFormFields = {
        address_line1: document.getElementById("address_line1"),
        address_line2: document.getElementById("address_line2"),
        city: document.getElementById("city"),
        state: document.getElementById("state"),
        postal_code: document.getElementById("postal_code"),
        country: document.getElementById("country"),
    };

    // Function to clear the address form
    function clearAddressForm() {
        Object.values(addressFormFields).forEach(field => {
            field.value = "";
            field.disabled = false;
        });
    }

    // Function to fill the address form with the selected address
    function fillAddressForm(addressData) {
        Object.keys(addressData).forEach(key => {
            if (addressFormFields[key]) {
                addressFormFields[key].value = addressData[key];
                addressFormFields[key].disabled = true;
            }
        });
    }

    // Add event listeners to the radio buttons
    addressInputs.forEach(input => {
        input.addEventListener("change", function () {
            if (this.checked) {
                if (this.dataset.address) {
                    const addressData = JSON.parse(this.dataset.address);
                    fillAddressForm(addressData);
                } else {
                    clearAddressForm();
                }
            }
        });
    });

    // Default to clearing the address form on load
    clearAddressForm();
});
