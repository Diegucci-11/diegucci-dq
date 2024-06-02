function onEdit(e) {
  var ss = e.source;
  var sheet = ss.getActiveSheet(); // Cogemos la referencia a la hoja activa
  var activeCell = e.range; // Cogemos la referencia a la celda activa

  if(sheet.getSheetName() === "Matriz_Input"){ // Comprobamos si estamos en esta hoja
    if(activeCell.getRow() >= 5 && activeCell.getColumn() === 1){ // Comprobamos si ha sucedido un cambio en la columna de tablas (Si el usuario a elegido alguna)
      if (activeCell.getValue() === "_") { // Si el valor de la lista desplegable es '_' 
        activeCell.offset(0, 1).clearDataValidations(); // Eliminamos la lista de validación de su celda derecha (campos)
        activeCell.offset(0, 7).clearDataValidations(); // Eliminamos la lista de validación de filtros

        var rangoFila = sheet.getRange(activeCell.getRow(), 1, 1, sheet.getLastColumn()); // Cogemos la referencia a la fila donde se encuentra
        rangoFila.clearContent(); // Borramos el contenido de la fila
        rangoFila.setBackground("white")
      }
      else{
        var hojaTablas = ss.getSheetByName('Tablas');
        var nombresTablas = hojaTablas.getRange('C14:C').getValues();
        var valor = activeCell.getValue();
        var fila = -1;

        for (var i = 0; i < nombresTablas.length; i++) {
          if (nombresTablas[i][0].trim() === valor.trim()) { 
            fila = i;
          }
        }

        var valoresColumna = hojaTablas.getRange(fila+14, 5).getValue().split(',');
        for (var i = 0; i < valoresColumna.length; i++) {
          valoresColumna[i] = valoresColumna[i].trim();
        }

        activeCell.offset(0, 1).clearDataValidations(); // Borrramos la lista desplegable de su derecha (campos)
        activeCell.offset(0, 1).clearContent(); // Y le borramos el contenido (para reemplazarlo por otro luego)
        var validacionCampos = SpreadsheetApp.newDataValidation().requireValueInList(valoresColumna).build(); // Creamos lista de validacion con esos campos
        activeCell.offset(0, 1).setDataValidation(validacionCampos); // Asignamos la lista de validación a la celda de al lado (campos)

        listas_filtros_matrix(ss, activeCell);
      }
    }
    if((activeCell.getRow() >= 5 && activeCell.getColumn() === 1) || (activeCell.getRow() >= 5 && activeCell.getColumn() === 2)){
      comprobarDuplicados(sheet);
    }
    if(activeCell.getRow() >= 5 && activeCell.getColumn() === 2){
      if(sheet.getRange(activeCell.getRow(), 1).getValue().trim() != ''){
        obtenerTipoDato(ss, activeCell.getRow(), sheet.getRange(activeCell.getRow(), 1).getValue(), sheet.getRange(activeCell.getRow(), 2).getValue());
      }
      var fila = activeCell.getRow();
      var reglasSheet = ss.getSheetByName("Reglas");
      var tipoDato = sheet.getRange(fila, 5).getValue();
      var numColumns = sheet.getLastColumn();
      var offset = 0;
      for (var j = 9; j <= numColumns; j++) {
        sheet.getRange(fila, j).setBackground("white");
        if(sheet.getRange(3, j).getValue().trim() === ''){
          offset++;
          if(sheet.getRange(fila, j-1).getBackgroundColor() === "#808080"){
            sheet.getRange(fila, j).setBackground("gray");
            sheet.getRange(fila, j).setValue(sheet.getRange(3, j).getValue().trim());
          }else{
            continue;
          }
        }
        else{
          var tipoDatoRegla = reglasSheet.getRange(j-6-offset, 5).getValue();
          if(tipoDato === "STRING"){
            if (tipoDatoRegla !== "CADENA" && tipoDatoRegla !== "TODOS") {
              sheet.getRange(fila, j).setBackground("gray");
            }
          }
          else if(tipoDato === "INTEGER" || tipoDato === "FLOAT"){
            if (tipoDatoRegla !== "NUMERICO" && tipoDatoRegla !== "TODOS") {
              sheet.getRange(fila, j).setBackground("gray");
            }
          }
          else if(tipoDato === "TIMESTAMP" || tipoDato === "DATETIME"){
            if (tipoDatoRegla !== "FECHA" && tipoDatoRegla !== "TODOS") {
              sheet.getRange(fila, j).setBackground("gray");
            }
          }
        } 
      }
    }
  }
  else if (sheet.getSheetName() === "Tablas"){
    var valoresLocalizaciones = (['northamerica-northeast1', 'northamerica-northeast2', 'southamerica-east1', 'southamerica-west1', 'us-central1', 
                                  'us-east1', 'us-east4', 'us-east5', 'us-south1',  'us-west1', 'us-west2', 'us-west3', 'us-west4', 'asia-east1', 
                                  'asia-east2', 'asia-northeast1', 'asia-northeast2', 'asia-northeast3', 'asia-south1', 'asia-south2', 'asia-southeast1', 
                                  'asia-southeast2', 'australia-southeast1', 'australia-southeast2', 'europe-central2', 'europe-north1', 'europe-southwest1', 
                                  'europe-west1', 'europe-west2', 'europe-west3', 'europe-west4', 'europe-west6', 'europe-west8', 'europe-west9', 
                                  'europe-west10', 'europe-west12', 'me-central1', 'me-central2', 'me-west1', 'africa-south1', 'aws-ap-northeast-2', 
                                  'aws-eu-west-1', 'aws-us-east-1', 'aws-us-west-2', 'azure-eastus2']);

    if (activeCell.getA1Notation() === 'B4' && activeCell.getValue() !== ""){ // Proyecto de GCP
      listas_bu(ss);
      listas_capas(ss);
      listas_entorno(ss);
      // listas_tipo_dato_matrix(ss); // AUTOMATIZADO! 
      listas_severidad(ss);
      listas_prioridad(ss);

      var validacionLocalizaciones = SpreadsheetApp.newDataValidation().requireValueInList(valoresLocalizaciones).build();
      sheet.getRange('B6').setDataValidation(validacionLocalizaciones);
    }
    // Nombre Localización
    else if(activeCell.getA1Notation() === 'B6' && activeCell.getValue() !== ""){ // Comprobamos si se ha elegido una localización
      nombreLocalizacion(valoresLocalizaciones, activeCell, sheet);
    }
    // Listas para Tablas
    else if(activeCell.getRow() >= 14 && activeCell.getColumn() === 3) { // Si se define una tabla nueva en 'Tablas'
      listas_tablas_matrix(ss);
      listas_tablas_filtros(ss);
      listas_filtros_matrix(ss, activeCell);
    }
  }
  else if (sheet.getSheetName() === "Filtros"){
    lista_campos_filtros(ss, activeCell);

    if(activeCell.getRow() >=3 && (activeCell.getColumn() === 1 || activeCell.getColumn() === 2)){
      if((sheet.getRange(activeCell.getRow(), 1).getValue() != "" && sheet.getRange(activeCell.getRow(), 2).getValue() != "") || 
        (activeCell.getColumn() === 1 && activeCell.getValue() === "_")){
          actualizar_filtros_matrix(ss);
      }
    }
  }
  else if (sheet.getName() == "Reglas" && activeCell.getRow() > 2) {
    var numFilasGuardadas = parseInt(PropertiesService.getScriptProperties().getProperty('numFilasReglas'));
    var matrizInputSheet = ss.getSheetByName("Matriz_Input");
    var numRowsAfterEdit = sheet.getLastRow();
    var fila = activeCell.getRow();
    if (numRowsAfterEdit > numFilasGuardadas) {
      var columnaMatriz = fila + 6; 
      
      matrizInputSheet.insertColumnAfter(columnaMatriz - 1);
      matrizInputSheet.getRange(2, columnaMatriz).setFormula('=Reglas!A' + fila);
      matrizInputSheet.getRange(3, columnaMatriz).setFormula('=Reglas!B' + fila);
      matrizInputSheet.getRange(3, columnaMatriz).setBackground('#84bf9e');
      matrizInputSheet.getRange(4, columnaMatriz).setBackground('#d0d3d4');
    }
    else if(activeCell.getColumn() == 6){
      var values = activeCell.getValue().split('\n');
      var numValues = values.length;
      
      var columnaMatriz = activeCell.getRow() + 6; 
      
      for (var i = 0; i < numValues; i++) {
        var value = values[i].trim().replace('-', '');

        if(matrizInputSheet.getRange(3, columnaMatriz + i).getValue() == "" || i==0){
          matrizInputSheet.getRange(4, columnaMatriz + i).setValue(value);
          matrizInputSheet.getRange(4, columnaMatriz + i).setBackground('#84bf9e');
          matrizInputSheet.getRange(3, columnaMatriz + i).setBackground('#009657');
        }
        else{
          matrizInputSheet.insertColumnAfter(columnaMatriz + i - 1);
          matrizInputSheet.getRange(2, columnaMatriz + i).setFormula('=' + String.fromCharCode(columnaMatriz + 64) + 2);
          matrizInputSheet.getRange(3, columnaMatriz + i).setFormula('=' + String.fromCharCode(columnaMatriz + 64) + 3);
          matrizInputSheet.getRange(4, columnaMatriz + i).setBackground('#84bf9e');
          matrizInputSheet.getRange(4, columnaMatriz + i).setValue(value);
          matrizInputSheet.getRange(3, columnaMatriz, 1, i + 1).mergeAcross();
        }
      }
    }
    // PENDIENTE DE INVESTIGAR! SEGURAMENTE LIMITACIÓN TECNICA
    // else if (numRowsAfterEdit < numFilasGuardadas) {
    //   matrizInputSheet.getRange("K10").setValue(numRowsAfterEdit + " || " + numFilasGuardadas);
    //   var columnaMatriz = activeCell.getRow() + 5;
    //   matrizInputSheet.deleteColumn("12");
    // }
    PropertiesService.getScriptProperties().setProperty('numFilasReglas', numRowsAfterEdit);
  }
}

function nombreLocalizacion(valoresLocalizaciones, activeCell, sheet){
  var nombreLocalizaciones = (['Montréal', 'Toronto', 'São Paulo', 'Santiago', 'Iowa', 'South Carolina', 'Northem Virginia', 'Columbus', 'Dallas', 
                              'Oregon', 'Los Angeles', 'Salt Lake City', 'Las Vegas', 'Taiwan', 'Hong Kong', 'Tokyo', 'Osaka', 'Seoul', 'Mumbai', 
                              'Delhi', 'Singapore', 'Jakarta', 'Sydney', 'Melbourne', 'Warsaw', 'Finland', 'Madrid', 'Belgium', 'London', 'Frankfurt',
                              'Netherlands', 'Zurich', 'Milan', 'Paris', 'Berlin', 'Turin', 'Doha', 'Dammam', 'Tel Aviv', 'Johannesburg', 'aws-ap-northeast-2', 
                              'aws-eu-west-1', 'aws-us-east-1', 'aws-us-west2', 'azure-eastus2']);

  for (var i = 0; i < valoresLocalizaciones.length; i++) {
    if (valoresLocalizaciones[i] === activeCell.getValue()) {
      sheet.getRange('C6').setValue(nombreLocalizaciones[i].toUpperCase()); // Ponemos la ciudad y país en mayúsculas al lado de la lista desplegable 
      break; 
    }
  }
}

function comprobarDuplicados(sheet){
  var data = sheet.getRange(5, 1, sheet.getLastRow()-1, 2).getValues(); // Cogemos los valores de las 2 primeras columnas

  sheet.getRange(5, 1, sheet.getLastRow()-1, 2).setBackground(null); // Quitamos el fondo a todas las filas
  
  for (var i = 0; i < data.length; i++) {
    var columna1 = data[i][0]; // Columna 1 (tabla)
    var columna2 = data[i][1]; // Columna 2 (campo)

    if (columna1 !== "" && columna2 !== "") {
      for (var j = i + 1; j < data.length; j++) { //Cogemos referencias a las siguientes filas
        var otraColumna1 = data[j][0];
        var otraColumna2 = data[j][1];
        
        if (columna1 === otraColumna1 && columna2 === otraColumna2) { // Comprobamos que son iguales
          sheet.getRange(j + 5, 1, 1, 2).setBackground('#FF0000'); // Nuevo registro que ya está repetido, en rojo
        }
      }
    }
  }
}

function actualizar_filtros_matrix(ss){
  var hoja_matrix = ss.getSheetByName('Matriz_Input');
  var hoja_filtros = ss.getSheetByName('Filtros');
  
  var tablasFiltros = hoja_filtros.getRange('A5:A').getValues();
  var tablas = [];
  
  for (var k = 0; k < tablasFiltros.length; k++) {
    var valoresEncontrados = ["NOT_NULL", "NO_FILTER"];
    nombre_tabla = tablasFiltros[k][0];
    if (tablas.indexOf(nombre_tabla) === -1 && nombre_tabla != "") {
      tablas.unshift([nombre_tabla]);
      
      for (var j = 0; j < tablasFiltros.length; j++){
        if (nombre_tabla === tablasFiltros[j][0]) {
          var nombre_filtro = hoja_filtros.getRange(j + 5, 2).getValue();
          valoresEncontrados.push(nombre_filtro);
        }
      }

      for (var i = 5; i < hoja_matrix.getLastRow(); i++){
        var listaF = SpreadsheetApp.newDataValidation().requireValueInList(valoresEncontrados).setAllowInvalid(false).build();
        if(nombre_tabla === hoja_matrix.getRange(i, 1).getValue()){
          hoja_matrix.getRange(i, 8).clearDataValidations();
          hoja_matrix.getRange(i, 8).setDataValidation(listaF);
        }
      }
    }
  }
}

function obtenerTipoDato(ss, row, nombre_tabla, nombre_campo) {
  var hojaMatrix = ss.getSheetByName("Matriz_Input");
  var tablasSheet = ss.getSheetByName("Tablas");
  var tablaRow = tablasSheet.createTextFinder(nombre_tabla).matchEntireCell(true).findNext().getRow();
  
  var nombresCampos = tablasSheet.getRange(tablaRow, 5).getValue().split(",");
  var index = nombresCampos.indexOf(nombre_campo);
  
  var tipoDato = tablasSheet.getRange(tablaRow, 6).getValue().split(",")[index];
  hojaMatrix.getRange(row, 5).setValue(tipoDato);
}









