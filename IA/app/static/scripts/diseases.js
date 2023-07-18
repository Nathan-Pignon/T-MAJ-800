$(document).ready(function() {

    $('#upload').click(function() {
        // Get the file from id file
        let file = $('#file')[0].files[0];
        // Create a FormData object
        let formData = new FormData();
        // Append the file to FormData object
        formData.append('file', file);
        // Send the file to the server
        $.ajax({
            url: '/diseases',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
                console.log(data)
            },
            error: function(err) {
                console.log(err)
            }
        });
    });

});