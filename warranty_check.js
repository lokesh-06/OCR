function doPost(e) {
    try {
      const sheet = SpreadsheetApp.openById('1Wlhl1wAVpJLg4JrdWKKgWYfnCE2WWuDtqD0naLxrkH0').getSheetByName('Warranty Info');
      const data = JSON.parse(e.postData.contents);
      const modelNumber = data.modelNumber;
      const invoiceDate = new Date(data.invoiceDate);
  
      Logger.log('Received modelNumber: ' + modelNumber);
      Logger.log('Received invoiceDate: ' + invoiceDate);
  
      const rows = sheet.getDataRange().getValues();
      for (let i = 1; i < rows.length; i++) {
        if (rows[i][0] === modelNumber) {
          const warrantyPeriod = rows[i][1];
          Logger.log('Warranty period for model: ' + warrantyPeriod);
  
          const warrantyEndDate = new Date(invoiceDate);
          warrantyEndDate.setMonth(warrantyEndDate.getMonth() + warrantyPeriod);
  
          Logger.log('Warranty end date: ' + warrantyEndDate);
  
          const currentDate = new Date();
          if (currentDate <= warrantyEndDate) {
            return ContentService.createTextOutput(JSON.stringify({"status": "under warranty"}))
                                 .setMimeType(ContentService.MimeType.JSON);
          } else {
            return ContentService.createTextOutput(JSON.stringify({"status": "out of warranty"}))
                                 .setMimeType(ContentService.MimeType.JSON);
          }
        }
      }
      return ContentService.createTextOutput(JSON.stringify({"status": "model not found"}))
                           .setMimeType(ContentService.MimeType.JSON);
    } catch (error) {
      Logger.log('Error: ' + error.message);
      return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": error.message}))
                           .setMimeType(ContentService.MimeType.JSON);
    }
  }
  
  