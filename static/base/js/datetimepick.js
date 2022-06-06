$(document).ready(function () {
    moment.locale('es', {
        week: {
            dow: 1
        } // Monday is the first day of the week
    });

    //Initialize the datePicker(I have taken format as mm-dd-yyyy, you can     //have your owh)
    $("#fechaInicioSemana").datetimepicker({
        format: 'DD/MM/YYYY'
    });

    //Get the value of Start and End of Week
    $('#fechaInicioSemana').on('dp.change', function (e) {
        var value = $("#fechaInicioSemana").val();
        var firstDate = moment(value, "DD/MM/YYYY").day(1).format("DD/MM/YYYY");
        var lastDate = moment(value, "DD/MM/YYYY").day(7).format("DD/MM/YYYY");
        $("#fechaInicioSemana").val(firstDate);
        $("#fechaFinalSemana").val(lastDate);
    });
});

