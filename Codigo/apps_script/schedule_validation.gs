function schedule_validation() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var hoja_matriz = ss.getSheetByName("Matriz_Input");
  
  var name = hoja_matriz.getRange("B2").getValue().toLowerCase();
  var cron = hoja_matriz.getRange("D2").getValue();

  if (name === '' || cron === '') {
    SpreadsheetApp.getUi().alert("Error: Debes completar el campo de 'Nombre Matriz' y Expresión CRON");
    return;
  }

  var data = {
    gs_name: ss.getName(),
    name: name,
    cron: cron
  };
  
  var url = "https://europe-southwest1-tfg-dq.cloudfunctions.net/schedule_validation";
  
  var options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(data)
  };
  
  try{
    var response = UrlFetchApp.fetch(url, options);
    var statusCode = response.getResponseCode();
    if (statusCode === 200) {
      SpreadsheetApp.getUi().alert("La programación se ha establecido con éxito. Espera 2 minutos para poder ejecutarlo bajo demanda.");
    }
    else{
      SpreadsheetApp.getUi().alert("Ha ocurrido un error inesperado, asegúrate de que los campos tenían un valor válido");
    }
  }
  catch (e){
    SpreadsheetApp.getUi().alert("Ha ocurrido un error inesperado, asegúrate de que los campos tenían un valor válido.");
    return;
  }
}

