function lista_campos_filtros(ss, activeCell) {
  var hoja_tablas = ss.getSheetByName('Tablas');
  var hoja_filtros = ss.getSheetByName('Filtros');

  if(activeCell.getRow() >= 5 && activeCell.getColumn() === 1){ // Comprobamos si ha sucedido un cambio en la columna de tablas (Si el usuario a elegido alguna)
      if (activeCell.getValue() === "_") { // Si el valor de la lista desplegable es '_' 
        activeCell.offset(0, 3).clearDataValidations(); // Eliminamos la lista de validación de su celda derecha (tipo de dato)
        activeCell.offset(0, 4).clearDataValidations(); // Eliminamos campo
        activeCell.offset(0, 5).clearDataValidations(); // Eliminamos Operacion

        var rangoFila = hoja_filtros.getRange(activeCell.getRow(), 1, 1, hoja_filtros.getLastColumn()); // Cogemos la referencia a la fila donde se encuentra
        rangoFila.clearContent(); // Borramos el contenido de la fila
        actualizar_filtros_matrix(ss);
      }
      else{
        var nombresTablas = hoja_tablas.getRange('C14:C').getValues();
        var valor = activeCell.getValue();
        var fila = -1;

        for (var i = 0; i < nombresTablas.length; i++) {
          if (nombresTablas[i][0].trim() === valor.trim()) { 
            fila = i;
          }
        }

        var valoresColumna = hoja_tablas.getRange(fila+14, 5).getValue().split(',');
        for (var i = 0; i < valoresColumna.length; i++) {
          valoresColumna[i] = valoresColumna[i].trim();
        }

        activeCell.offset(0, 4).clearDataValidations(); // Borrramos la lista desplegable de su derecha (campos)
        activeCell.offset(0, 4).clearContent(); // Y le borramos el contenido (para reemplazarlo por otro luego)
        var validacionCampos = SpreadsheetApp.newDataValidation().requireValueInList(valoresColumna).build(); // Creamos lista de validacion con esos campos
        activeCell.offset(0, 4).setDataValidation(validacionCampos); // Asignamos la lista de validación a la celda de al lado (campos)

        listas_tipo_dato_filtros(ss, activeCell);
      }
    }

  else if(activeCell.getRow() >= 5 && activeCell.getColumn() === 4){ // Listas desplegables de operaciones
    listas_operaciones(ss, activeCell);
  }
  // else if(activeCell.getRow() >= 5 && activeCell.getColumn() === 2){ // Filtros en Matrix_Input
  //   // listas_filtros_matrix(ss, activeCell);
  // }
}






