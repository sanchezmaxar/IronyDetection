function cambio() {
    // Para asignar un nuevo valor a la variable global "a" no se usa var, 
    // solo el nombre de la variable
    var cadena = $("#cadena").val();
    // console.log(cadena)
    remplazar(cadena);
};

function cambio2() {
    // Para asignar un nuevo valor a la variable global "a" no se usa var, 
    // solo el nombre de la variable
    var cadena = $("#cadena2").val();
    // console.log(cadena)
    remplazar(cadena);
};


function remplazar(cadena) {

    for (var i = 0; i < 4; i++) {
        modelo(cadena, i, i == 0 ? 100 : 200);

    }
}


function modelo(cadena, n, maxlen) {
    var data = { cadena: cadena, n: n, maxlen: maxlen }
    // var data = { cadena: "@ @ soy tu competencia Alicia jejeje 😈😈 " ,n:0,maxlen:100}
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "http://0.0.0.0:8090/postjson",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "cache-control": "no-cache",
            "Postman-Token": "c949041d-6ace-413e-a9ed-e554b1e713b8"
        },
        "processData": false,
        "data": JSON.stringify(data)
    }

    $.ajax(settings).done(function (response) {
        var respuesta = JSON.parse(response);
        document.getElementById(`exp${n + 1}_0`).innerText = JSON.stringify(respuesta['frase'])
        document.getElementById(`exp${n + 1}_1`).innerText = JSON.stringify(respuesta["vector"][0])
        document.getElementById(`exp${n + 1}_2`).innerText = respuesta["pred"]["outputs"][0][0]
        return true;
    });
}