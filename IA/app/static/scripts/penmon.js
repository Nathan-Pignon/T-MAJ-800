$(document).ready(function() {
    // When vineyard is selected, update latitude and altitude
    $('select').change(function() {
        let vineyard = $(this).val();
        let latitude = $('input[name="latitude"]');
        let altitude = $('input[name="altitude"]');
        $.ajax({
            url: '/penmon/vineyard/' + vineyard,
            type: 'GET',
            success: function(data) {
                // update value of latitude and altitude
                latitude.val(data.latitude);
                altitude.val(data.altitude);
                changeButtonStatus();
            },
            error: function() {
                latitude.val(0);
                altitude.val(0);
                changeButtonStatus();
            }
        });
    });

    // Enable / Disable button if all fields are filled
    $('input').keyup(function() {
        changeButtonStatus();
    });

    $('input').change(function() {
        changeButtonStatus();
    });

    let changeButtonStatus = () => {
        let vineyard = $('select').val();
        let latitude = $('input[name="latitude"]').val();
        let altitude = $('input[name="altitude"]').val();
        let date = $('input[name="date"]').val();
        if (vineyard && latitude && altitude && date) {
            $('#compute').removeAttr('disabled');
        } else {
            $('#compute').attr('disabled', 'disabled');
        }
    }

    $('#compute').click(function() {
        $('#results').addClass('d-none');
        $('#compute').attr('disabled', 'disabled');
        $('#compute-spin').removeClass('d-none');
        $.ajax({
            url: '/penmon',
            type: 'POST',
            contentType: 'application/json',
            accept: 'application/json',
            data: JSON.stringify({
                vineyard: $('select').val(),
                latitude: $('input[name="latitude"]').val(),
                altitude: $('input[name="altitude"]').val(),
                date: $('input[name="date"]').val()
            }),
            success: function (data) {
                $('#results').removeClass('d-none');
                $('#compute').removeAttr('disabled');
                $('#compute-spin').addClass('d-none');
                if (data) {
                    for (let key in data) {
                        for (let subKey in data[key]) {
                            if (key === 'day') {
                                $(`#day-${subKey}`).html(`~ ${data[key][subKey]} mm`);
                            } else {
                                let img = $('<img />').attr('src', '/static/' + data[key][subKey]);
                                img.css('width', 'inherit');
                                img.css('height', 'inherit');
                                img.addClass('img-fluid');
                                $(`#${key}-${subKey}`).empty().append(img);
                            }
                        }
                    }
                }
            },
            error: function(err) {
                $('#results').removeClass('d-none');
                $('#compute').removeAttr('disabled');
                $('#compute-spin').addClass('d-none');
            }
        });
    });
});