$(document).ready(function() {

    $('input').change(function() {
        changeButtonStatus();
    });

     let changeButtonStatus = () => {
        let file = $('input[name="file"]').val();
        if (file) {
            $('#upload').removeAttr('disabled');
        } else {
            $('#upload').attr('disabled', 'disabled');
        }
    }

    $('#upload').click(function() {
        $('#results').addClass('d-none');
        $('#upload').attr('disabled', 'disabled');
        $('#upload-spin').removeClass('d-none');

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
                // Display results section
                $('#results').removeClass('d-none');
                $('#upload').removeAttr('disabled');
                $('#upload-spin').addClass('d-none');
                if (data) {
                    // Display the result
                    $('#prediction').html(data.prediction);

                    // Empty confidences ul
                    $('#confidences').empty();
                    // Display confidences
                    data.confidences.map((confidence) => {
                        $('#confidences').append(
                            `<li class="list-group-item">
                                <b>${confidence.class}</b> 
                                - ${confidence.score}%
                            </li>`
                        );
                    })
                }
            },
            error: function(err) {
                $('#results').removeClass('d-none');
                $('#upload').removeAttr('disabled');
                $('#upload-spin').addClass('d-none');
            }
        });
    });

});