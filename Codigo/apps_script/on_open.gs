function onOpen() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var reglasSheet = ss.getSheetByName("Reglas");
  var numRows = reglasSheet.getLastRow();
  PropertiesService.getScriptProperties().setProperty('numFilasReglas', numRows);
}
