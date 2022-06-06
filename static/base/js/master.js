function abrir_modal_eliminacion(url) {    
	$('#eliminacion').load(url, function () {
        console.log(url);
		$(this).modal('show');
	});
}

function cerrar_modal_eliminacion() {
    console.log("Cerro modal")
	$('#eliminacion').modal('hide');
    location.reload()
}

function eliminar(id) {    
    $.ajax({
        data:{
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
        },                
        url: '/caja/caja/detalle_rendicion_anular_modal/' + id ,
        type: 'post',        
        success: function (response) {
            console.log("llego a success")          
            cerrar_modal_eliminacion()  
        },
        error: function (error) {
            console.log("llego a error" + error);
            $('#error').html(error);            
        }
    });
}

function notificacionError(mensaje){
	Swal.fire({
		title: 'Error!',
		text: mensaje,
		icon: 'error'
	})
}

function notificacionSuccess(mensaje) {
	Swal.fire({
		title: 'Buen Trabajo!',
		text: mensaje,
		icon: 'success'
	})
}