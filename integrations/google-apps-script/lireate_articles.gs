/** Google Apps Script web app. Use Script Properties: SPREADSHEET_ID, SHEET_NAME, WEBHOOK_SECRET. */
function doPost(e) {
  function respond(value) {
    return ContentService.createTextOutput(JSON.stringify(value)).setMimeType(ContentService.MimeType.JSON);
  }
  const props = PropertiesService.getScriptProperties();
  let data;
  try { data = JSON.parse(e.postData.contents); }
  catch (err) { return respond({ok:false,error:"bad_json"}); }
  const secret = props.getProperty("WEBHOOK_SECRET");
  if (!secret || String(data.secret || "") !== secret) return respond({ok:false,error:"unauthorized"});
  const title = String(data.title || "").trim().slice(0,240);
  const url = String(data.url || "").trim();
  const summary = String(data.summary || "").replace(/<[^>]*>/g," ").replace(/\s+/g," ").trim().slice(0,600);
  if (!title || !summary || !/^https?:\/\/lireate\.ru\/[\w\-\/]+(?:\?.*)?$/i.test(url))
    return respond({ok:false,error:"invalid_data"});
  // Escape spreadsheet formulas provided through user/content fields.
  const safe = value => /^[=+\-@]/.test(value) ? "'" + value : value;
  const id = props.getProperty("SPREADSHEET_ID");
  const name = props.getProperty("SHEET_NAME") || "Статьи блога";
  if (!id) return respond({ok:false,error:"missing_sheet_id"});
  const lock = LockService.getScriptLock();
  lock.waitLock(25000);
  try {
    const sheet = SpreadsheetApp.openById(id).getSheetByName(name);
    if (!sheet) return respond({ok:false,error:"missing_tab"});
    const last = sheet.getLastRow();
    if (last < 1) return respond({ok:false,error:"missing_headers"});
    const headers = sheet.getRange(1,1,1,4).getDisplayValues()[0];
    if (headers.join("|") !== ["№","Название","Ссылка","О чём статья"].join("|"))
      return respond({ok:false,error:"headers_changed"});
    const records = last>1 ? sheet.getRange(2,1,last-1,4).getValues() : [];
    const normalize = s => String(s || "").trim().replace(/\/$/,"").toLowerCase();
    const i = records.findIndex(row => normalize(row[2]) === normalize(url));
    if (i !== -1) {
      sheet.getRange(i+2,2).setValue(safe(title));
      sheet.getRange(i+2,4).setValue(safe(summary));
      return respond({ok:true,action:"updated",row:i+2});
    }
    const highest = records.reduce((acc,row)=> Math.max(acc, Number(row[0]) || 0),0);
    sheet.appendRow([highest+1,safe(title),url,safe(summary)]);
    return respond({ok:true,action:"inserted",row:sheet.getLastRow()});
  } catch (err) {
    return respond({ok:false,error:"sheet_write_failed"});
  } finally {
    lock.releaseLock();
  }
}
