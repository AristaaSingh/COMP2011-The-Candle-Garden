// cookies javascript, mosty taken from course material Section 12- Cookies and Sessions

window.addEventListener("load", function () {
    window.cookieconsent.initialise({
        "palette": {
            "popup": {
                "background": "#eaf7f7",
                "text": "#5c7291"
            },
            "button": {
                "background": "#56cbdb",
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
