// cookies javascript, mosty taken from course material Section 12- Cookies and Sessions

window.addEventListener("load", function () {
    window.cookieconsent.initialise({
        "palette": {
            "popup": {
                "background": "#fdf6f0",
                "text": "#5a5a5a"
            },
            "button": {
                "background": "#d4a373",
                "text": "#ffffff"
            }
        },
        "content": {
            "message": "This website uses cookies.",
            "dismiss": "Great!",
            "href": "/cookie-policy"
        }
    });
});
