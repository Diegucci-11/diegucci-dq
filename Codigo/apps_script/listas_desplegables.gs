function listas_tipo_dato_matrix(ss){
  var hojaMatrizInput = ss.getSheetByName('Matriz_Input');
  var valoresTipoDato = (["INT64", "FLOAT64", "STRING", "TIMESTAMP", "DATETIME", "DATE"]); // VALORES Tipo de dato
  var rangoCapas = hojaMatrizInput.getRange(5, 5, 45, 1); 
  var validationRuleCapas = SpreadsheetApp.newDataValidation().requireValueInList(valoresTipoDato).build();
  rangoCapas.setDataValidation(validationRuleCapas);
}

function listas_tipo_dato_filtros(ss, activeCell){
  var valoresTipoDato = (['NUMÉRICO', 'CADENA', 'FECHA']);
  var valiacionTipoDato = SpreadsheetApp.newDataValidation().requireValueInList(valoresTipoDato).build();
  activeCell.offset(0, 3).setDataValidation(valiacionTipoDato);
}

function listas_prioridad(ss){
  var hojaMatrizInput = ss.getSheetByName('Matriz_Input');
  var valoresPrioridad = (["BAJA", "MEDIA", "ALTA"]); // VALORES Prioridad
  var rangoCapas = hojaMatrizInput.getRange(5, 4, 45, 1); 
  var validationRuleCapas = SpreadsheetApp.newDataValidation().requireValueInList(valoresPrioridad).build();
  rangoCapas.setDataValidation(validationRuleCapas);
}

function listas_entorno(ss){
  var hojaTablas = ss.getSheetByName('Tablas'); // Referencia a la hoja Tablas
  var hojaCorreos = ss.getSheetByName('Correos'); // Referencia a la hoja Correos
  var valoresEntorno = (['dev', 'test', 'pro']); // VALORES Entorno
  var rangoEntorno1 = hojaTablas.getRange(3, 2); // Rango para desplegar esas listas en Tablas
  var rangoEntorno2 = hojaCorreos.getRange(3, 3, 52, 1); // Rango para desplegar esas listas en Correos
  var validacionEntorno = SpreadsheetApp.newDataValidation().requireValueInList(valoresEntorno).build(); // Creación de la lista
  rangoEntorno1.setDataValidation(validacionEntorno); // Asignación de la lista en Tablas
  rangoEntorno2.setDataValidation(validacionEntorno); // Asignación de la lista en Correos
}

function listas_severidad(ss){
  var hojaInstrucciones = ss.getSheetByName('Instrucciones'); // Referencia a la hoja Matriz_Input
  var hojaCorreos = ss.getSheetByName('Correos'); // Referencia a la hoja Correos
  var hojaReglas = ss.getSheetByName('Reglas'); // Referencia a la hoja Reglas
  var valoresSeveridad = hojaInstrucciones.getRange(31, 2, 3).getValues(); // VALORES SEVERIDAD
  var rangoSeveridad1 = hojaCorreos.getRange(3, 4, 52 ,1); // Rango para desplegar esas listas en Correos
  var rangoSeveridad2 = hojaReglas.getRange(3, 7, 10, 1); // Rango para desplegar esas listas en Reglas
  var validacionSeveridad = SpreadsheetApp.newDataValidation().requireValueInList(valoresSeveridad).build(); // Creación de la lista
  rangoSeveridad1.setDataValidation(validacionSeveridad); // Asignación de la lista en Correos
  rangoSeveridad2.setDataValidation(validacionSeveridad); // Asignación de la lista en Reglas
}

function listas_bu(ss) {
  var hojaMatrizInput = ss.getSheetByName('Matriz_Input'); // Referencia a la hoja Matriz_Input
  var valoresBU = (['ES', 'FR']); // VALORES BU
  var rangoBU = hojaMatrizInput.getRange(5, 7, 45, 1); // Rango para desplegar esas listas
  var validacionBU = SpreadsheetApp.newDataValidation().requireValueInList(valoresBU).build(); // Creación de la lista
  rangoBU.setDataValidation(validacionBU); // Asignación de la lista
}

function listas_capas(ss){
  var hojaMatrizInput = ss.getSheetByName('Matriz_Input');
  var valoresCapas = (["BRONZE", "SILVER", "GOLDEN"]); // VALORES CAPAS
  var rangoCapas = hojaMatrizInput.getRange(5, 6, 45, 1); 
  var validationRuleCapas = SpreadsheetApp.newDataValidation().requireValueInList(valoresCapas).build();
  rangoCapas.setDataValidation(validationRuleCapas);
}

function listas_tablas_matrix(ss){
  var hojaMatrizInput = ss.getSheetByName('Matriz_Input');
  var hojaTablas = ss.getSheetByName('Tablas');
  var valoresTablas = hojaTablas.getRange(14, 3, hojaTablas.getLastRow() - 13).getValues(); // row, col, num_rows (últ con contenido - desde la que empezamos), num_cols
  valoresTablas.unshift(["_"]); // Añadimos este valor como primera opcion a la lista de valores 
  
  // Lista Tablas Matriz_Input
  var rangoMatrizInput = hojaMatrizInput.getRange(5, 1, 46, 1); // Rango donde asignaremos las listas desplegables de tablas en Matriz_Input
  var validacionTablas = SpreadsheetApp.newDataValidation().requireValueInList(valoresTablas).build();
  rangoMatrizInput.setDataValidation(validacionTablas);
}

function listas_tablas_filtros(ss){
  var hojaFiltros = ss.getSheetByName('Filtros');
  var hojaTablas = ss.getSheetByName('Tablas');
  var valoresTablas = hojaTablas.getRange(14, 3, hojaTablas.getLastRow() - 13, 1).getValues(); // row, col, num_rows (últ con contenido - desde la que empezamos), num_cols
  valoresTablas.unshift(["_"]); // Añadimos este valor como primera opcion a la lista de valores 
  
  // Lista Tablas Filtros
  var rangoHojaFiltros = hojaFiltros.getRange(5, 1, 5, 1); // Rango donde asignaremos las listas desplegables de tablas en Matriz_Input
  var validacionTablas = SpreadsheetApp.newDataValidation().requireValueInList(valoresTablas).build();
  rangoHojaFiltros.setDataValidation(validacionTablas);
}

function listas_filtros_matrix(ss, activeCell){
  var hojaMatrizInput = ss.getSheetByName('Matriz_Input');
  var hojaFiltros = ss.getSheetByName('Filtros');

  // Borramos el contenido que hubiese en la celda
  hojaMatrizInput.getRange(activeCell.getRow(), 8).clearContent(); 
  hojaMatrizInput.getRange(activeCell.getRow(), 8).clearDataValidations(); 

  var valorBuscado = hojaMatrizInput.getRange(activeCell.getRow(), 1).getValue();
  var tablasFiltros = hojaFiltros.getRange('A:A').getValues();

  var valoresEncontrados = [];

  for (var i = 0; i < tablasFiltros.length; i++) {
    if (tablasFiltros[i][0] === valorBuscado) {
      var valorObtenido = hojaFiltros.getRange(i + 1, 2).getValue();
      valoresEncontrados.push(valorObtenido);
    }
  }
  valoresEncontrados.unshift(["NOT_NULL"]);
  valoresEncontrados.unshift(["NO_FILTER"]);
  var listaF = SpreadsheetApp.newDataValidation().requireValueInList(valoresEncontrados).setAllowInvalid(false).build();
  hojaMatrizInput.getRange(activeCell.getRow(), 8).setDataValidation(listaF);   
  hojaMatrizInput.getRange(activeCell.getRow(), 8).setValue("NO_FILTER");
}

function listas_operaciones(ss, activeCell){
  var hojaFiltros = ss.getSheetByName('Filtros');
  var valores_numerico = (['igual a (número)', 'mayor o igual que', 'mayor que', 'menor que', 'menor o igual que']);
  var valores_string = (["igual a (cadena)", 'contiene subcadena', 'empieza por', 'acaba por']);

  var valores_fecha = (['mayor o igual que', 'mayor que', 'menor que', 'menor o igual que']); 
  var rangoOperaciones = hojaFiltros.getRange(activeCell.getRow(), 6); 
  var valiacionOperaciones;
  if(hojaFiltros.getRange(activeCell.getRow(), 4).getValue() === 'NUMÉRICO'){
    valiacionOperaciones = SpreadsheetApp.newDataValidation().requireValueInList(valores_numerico).build();
  }
  else if(hojaFiltros.getRange(activeCell.getRow(), 4).getValue() === 'CADENA'){
    valiacionOperaciones = SpreadsheetApp.newDataValidation().requireValueInList(valores_string).build();
  }
  else if(hojaFiltros.getRange(activeCell.getRow(), 4).getValue() === 'FECHA'){
    valiacionOperaciones = SpreadsheetApp.newDataValidation().requireValueInList(valores_fecha).build();
  }
  rangoOperaciones.setDataValidation(valiacionOperaciones); 
}



