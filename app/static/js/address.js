// this script handles automatic form filling when user wants to select an address from their list of saved addressed during checkout

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
    // fnction to clear the address form
    function clearAddressForm() {
        Object.values(addressFormFields).forEach(field => {
            field.value = "";
            field.disabled = false;
        });
    }
    // function to fill the adress automatically with the selection
    function fillAddressForm(addressData) {
        Object.keys(addressData).forEach(key => {
            if (addressFormFields[key]) {
                addressFormFields[key].value = addressData[key];
                addressFormFields[key].disabled = true;
            }
        });
    }
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
    clearAddressForm();
});
