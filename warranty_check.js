function doPost(e) {
    const sheet = SpreadsheetApp.openById('1Wlhl1wAVpJLg4JrdWKKgWYfnCE2WWuDtqD0naLxrkH0').getSheetByName('Warranty Info');
    const data = JSON.parse(e.postData.contents);
    const productCode = data.productCode;
    const invoiceDate = new Date(data.invoiceDate);

    const rows = sheet.getDataRange().getValues();
    for (let i = 1; i < rows.length; i++) {
        if (rows[i][1] === productCode) { // Assuming the Product Code is in the second column (index 1)
            const warrantyPeriod = rows[i][2]; // Assuming the Warranty Period is in the third column (index 2)
            const warrantyEndDate = new Date(invoiceDate);
            warrantyEndDate.setMonth(warrantyEndDate.getMonth() + warrantyPeriod);

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
    return ContentService.createTextOutput(JSON.stringify({"status": "product code not found"}))
                         .setMimeType(ContentService.MimeType.JSON);
}
