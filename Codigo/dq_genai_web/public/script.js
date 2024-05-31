var rule_input = document.getElementById('rule_input');
var create_rule = document.getElementById('create_rule');
create_rule.disabled = true;

var json_rule = {}

rule_input.addEventListener('input', function () {
    if (rule_input.value.trim() === '') {
        create_rule.disabled = true;
    } else {
        create_rule.disabled = false;
    }
});

function generarRegla() {
    var texto = document.getElementById('rule_input').value;
    var radioSeleccionado = document.querySelector('input[name="dim"]:checked').value;
    create_rule.disabled = true;
    console.log("Se está generando la regla...")

    var load_circle = document.getElementById('load-circle');
    load_circle.style.display = 'block';

    var datos = {
        "prompt": texto,
        "dimension": radioSeleccionado
    };

    fetch('https://europe-southwest1-tfg-dq.cloudfunctions.net/create_rule_2', {
        method: 'POST',
        // headers: {
        //     'Content-Type': 'application/json'
        // },
        body: JSON.stringify(datos)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Hubo un problema con la solicitud.');
            }
            load_circle.style.display = 'none';
            return response.json();
        })
        .then(data => {
            console.log('Se generó la regla');
            console.log(data)
            json_rule = JSON.parse(data)
            procesarRegla(json_rule)
            create_rule.disabled = false;
            load_circle.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            load_circle.style.display = 'none';
        });
}

function procesarRegla(data) {
    var content = document.getElementById('content');

    // Crear la tabla
    tabla = document.createElement('table');
    tabla.setAttribute('id', 'rule_results');

    // Crear contenido tabla
    const tbody = document.createElement('tbody');

    // CABECERA!
    const fila_cabecera = document.createElement('tr');
    const celda_cabecera = document.createElement('td');
    celda_cabecera.setAttribute('colspan', '4');
    const div_cabecera = document.createElement('div');
    div_cabecera.setAttribute('id', 'nombre_regla');
    div_cabecera.textContent = data["NOMBRE_REGLA_YML"];
    celda_cabecera.appendChild(div_cabecera);
    fila_cabecera.appendChild(celda_cabecera);

    // Fila 1 de la tabla
    const fila1 = document.createElement('tr');
    const celda_dim_title = document.createElement('td');
    const celda_name_title = document.createElement('td');
    celda_dim_title.setAttribute('class', 'rule_schema');
    celda_name_title.setAttribute('class', 'rule_schema');
    celda_dim_title.textContent = "Dimensión: ";
    celda_name_title.textContent = "Nombre de la regla: ";

    const celda_dim = document.createElement('td');
    celda_dim.setAttribute('class', 'rule_content');
    const select_dim = document.createElement('select');
    select_dim.setAttribute('id', 'rule_dim');

    const options_dim = ['Completitud', 'Consistencia', 'Exactitud', 'Integridad', 'Unicidad', 'Validez', 'Disponibilidad'];
    options_dim.forEach(opcion => {
        const option = document.createElement('option');
        option.text = opcion;
        select_dim.add(option);
    });
    const value_dim = data["DIMENSION"];
    select_dim.value = value_dim;
    celda_dim.appendChild(select_dim);


    const celda_name = document.createElement('td');
    celda_name.setAttribute('class', 'rule_content');
    const div_name = document.createElement('div');
    div_name.setAttribute('id', 'rule_name');
    div_name.setAttribute('class', 'div_content');
    div_name.setAttribute('oninput', 'actualizarNombre()');
    div_name.setAttribute('contenteditable', 'true');
    div_name.textContent = data["NOMBRE_REGLA_YML"];
    celda_name.appendChild(div_name);

    fila1.appendChild(celda_dim_title);
    fila1.appendChild(celda_dim);
    fila1.appendChild(celda_name_title);
    fila1.appendChild(celda_name);

    // Fila 2 de la tabla
    const fila2 = document.createElement('tr');
    const celda_desc_title = document.createElement('td');
    const celda_example_title = document.createElement('td');
    celda_desc_title.setAttribute('class', 'rule_schema');
    celda_example_title.setAttribute('class', 'rule_schema');
    celda_desc_title.textContent = "Descripción: ";
    celda_example_title.textContent = "Ejemplo: ";

    const celda_desc = document.createElement('td');
    celda_desc.setAttribute('class', 'rule_content');
    const div_desc = document.createElement('div');
    div_desc.setAttribute('id', 'rule_desc');
    div_desc.setAttribute('class', 'div_content');
    div_desc.setAttribute('contenteditable', 'true');
    div_desc.textContent = data["DESCRIPCION"];
    celda_desc.appendChild(div_desc);

    const celda_example = document.createElement('td');
    celda_example.setAttribute('class', 'rule_content');
    const div_example = document.createElement('div');
    div_example.setAttribute('id', 'rule_example');
    div_example.setAttribute('class', 'div_content');
    div_example.setAttribute('contenteditable', 'true');
    div_example.textContent = data["EJEMPLO"];
    celda_example.appendChild(div_example);

    fila2.appendChild(celda_desc_title);
    fila2.appendChild(celda_desc);
    fila2.appendChild(celda_example_title);
    fila2.appendChild(celda_example);

    // Fila 3 de la tabla
    const fila3 = document.createElement('tr');
    const celda_sev_title = document.createElement('td');
    const celda_action_title = document.createElement('td');
    celda_sev_title.setAttribute('class', 'rule_schema');
    celda_action_title.setAttribute('class', 'rule_schema');
    celda_sev_title.textContent = "Severity: ";
    celda_action_title.textContent = "Action: ";

    const celda_sev = document.createElement('td');
    celda_sev.setAttribute('class', 'rule_content');

    const celda_action = document.createElement('td');
    celda_action.setAttribute('class', 'rule_content');

    // Creacion lista desplegable para severidad
    const select_sev = document.createElement('select');
    select_sev.setAttribute('id', 'rule_sev');

    const options_sev = ['1 (Baja)', '2 (Media)', '3 (Alta)'];
    options_sev.forEach(opcion => {
        const option = document.createElement('option');
        option.text = opcion;
        select_sev.add(option);
    });
    const value_sev = '2 (Media)';
    select_sev.value = value_sev;
    celda_sev.appendChild(select_sev);

    // Creacion lista desplegable para accion
    const select_action = document.createElement('select');
    select_action.setAttribute('id', 'rule_action');

    const options_action = ['1 (Parada)', '2 (Notificación)', '3 (No Notifica)'];
    options_action.forEach(opcion => {
        const option = document.createElement('option');
        option.text = opcion;
        select_action.add(option);
    });
    const value_action = '2 (Notificación)';
    select_action.value = value_action;
    celda_action.appendChild(select_action);

    fila3.appendChild(celda_sev_title);
    fila3.appendChild(celda_sev);
    fila3.appendChild(celda_action_title);
    fila3.appendChild(celda_action);

    // Fila 4 de la tabla
    const fila4 = document.createElement('tr');
    const celda_tipo_dato_title = document.createElement('td');
    const celda_yml_title = document.createElement('td');
    celda_tipo_dato_title.setAttribute('class', 'rule_schema');
    celda_yml_title.setAttribute('class', 'rule_schema');
    celda_tipo_dato_title.textContent = "Tipo de Dato: ";
    celda_yml_title.textContent = "Código yaml: ";

    //  --------------------------------------------
    const celda_tipo_dato = document.createElement('td');
    celda_tipo_dato.setAttribute('class', 'rule_content');
    const div_tipo_dato = document.createElement('div');
    div_tipo_dato.setAttribute('id', 'rule_tipo_dato');
    div_tipo_dato.setAttribute('class', 'div_content_2');
    div_tipo_dato.setAttribute('contenteditable', 'true');
    div_tipo_dato.textContent = data["TIPO_DATO"];
    celda_tipo_dato.appendChild(div_tipo_dato);
    // .............................................
    // const celda_tipo_dato = document.createElement('td');
    // celda_tipo_dato.setAttribute('class', 'rule_content');
    // // Creacion lista desplegable para tipo de dato
    // const select_tipo_dato = document.createElement('select');
    // select_tipo_dato.setAttribute('id', 'rule_tipo_dato');

    // const options_tipo_dato = ['TODOS', 'CADENA', 'NUMERICO', 'FECHA'];
    // options_tipo_dato.forEach(opcion => {
    //     const option = document.createElement('option');
    //     option.text = opcion;
    //     select_tipo_dato.add(option);
    // });
    // const value_tipo_dato = data["TIPO_DATO"];
    // select_tipo_dato.value = value_tipo_dato;
    // celda_tipo_dato_title.appendChild(select_tipo_dato);
    //  --------------------------------------------

    const celda_yml = document.createElement('td');
    celda_yml.setAttribute('class', 'rule_content');
    const div_yml = document.createElement('div');
    div_yml.setAttribute('id', 'rule_yaml');
    div_yml.setAttribute('class', 'div_content_2');
    div_yml.setAttribute('contenteditable', 'true');
    div_yml.textContent = data["CODIGO_YML"];
    celda_yml.appendChild(div_yml);

    fila4.appendChild(celda_tipo_dato_title);
    fila4.appendChild(celda_tipo_dato);
    fila4.appendChild(celda_yml_title);
    fila4.appendChild(celda_yml);

    // Añadir filas al contenido de la tabla
    tbody.appendChild(fila_cabecera);
    tbody.appendChild(fila1);
    tbody.appendChild(fila2);
    tbody.appendChild(fila3);
    tbody.appendChild(fila4);

    tabla.appendChild(tbody);

    // Crear div que contiene botones
    const div_buttons = document.createElement('div');
    div_buttons.setAttribute('id', 'div_buttons');

    // Crear boton de append_rule
    const append_button = document.createElement('button');
    append_button.setAttribute('id', 'append_button');
    append_button.setAttribute('onclick', 'recogerValores()');

    append_button.textContent = "Añadir regla a Proyecto";

    // Crear boton de cancelar
    const cancel_button = document.createElement('button');
    cancel_button.setAttribute('id', 'cancel_button');
    cancel_button.setAttribute('onclick', 'resetearValores()');

    cancel_button.textContent = "Cancelar Regla";

    // Añadir boton al div
    div_buttons.appendChild(append_button);
    div_buttons.appendChild(cancel_button);

    // Logica para borrar el box_div si ya existe y que no se generen mas por cada regla que se genere
    var box_div = document.getElementById('rule_results_div');
    if (!box_div) {
        box_div = document.createElement('div');
        box_div.setAttribute('id', 'rule_results_div');
        box_div.setAttribute('class', 'box');
    } else {
        var tablaAnterior = document.getElementById('rule_results');
        var div_buttonsAnterior = document.getElementById('div_buttons');
        if (tablaAnterior) {
            box_div.removeChild(tablaAnterior);
            box_div.removeChild(div_buttonsAnterior);
        }
    }
    box_div.appendChild(tabla);
    box_div.appendChild(div_buttons);
    content.appendChild(box_div);
}

// Funcion para recoger los valores de la tabla rule_results
function recogerValores() {
    var rule_dim = document.getElementById('rule_dim').value;
    var rule_name = document.getElementById('rule_name').textContent;
    var rule_desc = document.getElementById('rule_desc').textContent;
    var rule_example = document.getElementById('rule_example').textContent;
    var rule_tipo_dato = document.getElementById('rule_tipo_dato').textContent;
    var rule_yaml = document.getElementById('rule_yaml').textContent;
    var rule_action = document.getElementById('rule_action').value;
    var rule_sev = document.getElementById('rule_sev').value;

    console.log("Valor de json_rule:\n")
    console.log(json_rule)

    var data = {
        "DIMENSION": rule_dim,
        "NOMBRE_REGLA_YML": rule_name,
        "DESCRIPCION": rule_desc,
        "EJEMPLO": rule_example,
        "TIPO_DATO": rule_tipo_dato,
        "PARAMETROS": json_rule["PARAMETROS"],
        "SEVERIDAD": rule_sev,
        "ACCION": rule_action,
        "CODIGO_YML": rule_yaml,
        "TIPO_REGLA_YML": rule_name
    }

    // Llamar a función append_rule
    fetch('https://europe-southwest1-tfg-dq.cloudfunctions.net/append_rule_2', {
        method: 'POST',
        // headers: {
        //     'Content-Type': 'application/json'
        // },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Hubo un problema con la solicitud.');
            }
            console.log(data)
            return response.json();
        })
        .then(data => {
            console.log(data)
            console.log('Regla insertada correctamente');
        })
        .catch(error => {
            console.log(data)
            console.error('Error:', error);
        });
}

function actualizarNombre() {
    var valorNombre = document.getElementById("rule_name").innerText;
    document.getElementById("nombre_regla").innerText = valorNombre;
}

function resetearValores() {
    console.log("Reseteando valores...")
    rule_input.value = "";

    var box_div = document.getElementById('rule_results_div');
    if (box_div) {
        box_div.remove();
    }

    var radioButtons = document.querySelectorAll('input[type="radio"][name="dim"]');

    radioButtons.forEach(function (radioButton) {
        if (radioButton.value === "Completitud") {
            radioButton.checked = true;
        } else {
            radioButton.checked = false;
        }
    });
}
