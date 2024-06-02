function trigger_validation() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var hoja_matriz = ss.getSheetByName("Matriz_Input");
  
  var name = hoja_matriz.getRange("B2").getValue().toLowerCase();

  if (name === '') {
    SpreadsheetApp.getUi().alert("Error: Debes completar el campo de 'Nombre Matriz' y el Flujo debe estar creado previamente.");
    return;
  }

  var data = {
    gs_name: ss.getName(),
    name: name
  };
  
  var url = "https://europe-southwest1-tfg-dq.cloudfunctions.net/dq_validation";
  
  var options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(data)
  };
  
  try{
    var response = UrlFetchApp.fetch(url, options);
    var statusCode = response.getResponseCode();
    if (statusCode === 200) {
      SpreadsheetApp.getUi().alert("El flujo ha sido ejecutado con éxito. Espera unos minutos para poder ver los resultados en Looker Studio.");
    }
    else{
      SpreadsheetApp.getUi().alert("Ha ocurrido un error inesperado, asegúrate de que los campos tenían un valor válido");
    }
  }
  catch (e){
    SpreadsheetApp.getUi().alert("Flujo no encontrado. Asegurate de que el flujo ha sido creado. Si el flujo ha sido creado hace poco, debes esperar unos minutos.");
    return;
  }
}
