function cargar_datos() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var tablasSheet = ss.getSheetByName("Tablas");
  
  var project_id_value = tablasSheet.getRange("B8").getValue();
  var dq_dataset_value = tablasSheet.getRange("B5").getValue();

  if (project_id_value === '' || dq_dataset_value === '') {
    SpreadsheetApp.getUi().alert('Error: Debes completar el campo de project_id y Dataset GCP DGQOffice asignado al producto. Por favor, completa los campos requeridos.');
    return;
  }

  var lastRow = tablasSheet.getLastRow() + 1;

  var data = {
    project_id: project_id_value,
    fila: lastRow,
    dq_dataset: dq_dataset_value,
    gs_name: ss.getName()
  };
  
  var url = "https://europe-southwest1-tfg-dq.cloudfunctions.net/config_gs";
  
  var options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(data)
  };
  
  var response = UrlFetchApp.fetch(url, options);
  
  Logger.log(response.getContentText());
  tablasSheet.getRange("B8").setValue("");
  listas_tablas_matrix(ss);
  listas_tablas_filtros(ss);
  // listas_filtros_matrix(ss, activeCell);
}
