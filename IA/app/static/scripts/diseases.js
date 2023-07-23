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
        $('#error').addClass('d-none');

        // Get the file from id file
        let file = $('#file')[0].files[0];
        // Create a FormData object
        let formData = new FormData();
        // Append the file to FormData object
        formData.append('file', file);
        // Append model to FormData object
        formData.append('model', $('#model').val());
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
                    });

                    if (data.image) {
                        // Display uploaded image
                        let img = $('<img />').attr('src', data.image);
                        img.css('width', 'inherit');
                        img.css('height', 'inherit');
                        img.addClass('img-fluid');

                        $('#uploaded-image').empty().append(img);
                    }

                    if (data.heatmaps) {
                        // Display heatmaps generated on uploaded image
                        let heatmaps = $('<img />').attr('src', data.heatmaps);
                        heatmaps.css('width', 'inherit');
                        heatmaps.css('height', 'inherit');
                        heatmaps.addClass('img-fluid');

                        $('#heatmaps').empty().append(heatmaps);
                    }
                }
            },
            error: function(err) {
                if (err.responseJSON.message) {
                    $('#error').empty().append(`<p class="m-0">${err.responseJSON.message}</p>`).removeClass('d-none');
                }

                $('#results').addClass('d-none');
                $('#upload').attr('disabled', 'disabled');
                $('#upload-spin').addClass('d-none');
            }
        });
    });

});