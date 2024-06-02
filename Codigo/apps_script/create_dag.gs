function create_dag() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var hoja_matriz = ss.getSheetByName("Matriz_Input");
  
  var dag_name = hoja_matriz.getRange("B2").getValue().toLowerCase();
  var dag_cron = hoja_matriz.getRange("D2").getValue();

  if (dag_name === '' || dag_cron === '') {
    SpreadsheetApp.getUi().alert("Error: Debes completar el campo de 'Nombre Matriz' y Expresión CRON");
    return;
  }

  var data = {
    dag_name: dag_name,
    dag_cron: dag_cron
  };
  
  var url = "https://europe-southwest1-tfg-dq.cloudfunctions.net/create_dag_dq";
  
  var options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(data)
  };
  
  try{
    var response = UrlFetchApp.fetch(url, options);
    var statusCode = response.getResponseCode();
    if (statusCode === 200) {
      SpreadsheetApp.getUi().alert("El flujo ha sido creado con éxito. Espera unos minutos para poder ejecutarlo bajo demanda.");
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
