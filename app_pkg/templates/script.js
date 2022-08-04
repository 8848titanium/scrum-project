function validateForm() {
    var name = document.forms["myForm"]["username"].value;
    var password = document.forms["myForm"]["password"].value;


    if (name == "") {
    alert("Name must be filled out");
    return false;
    }  if (password == "") {
    alert("Password must be filled out");
    return false;
    } }

    function showMessage(prompt) {
        alert(prompt);
                }