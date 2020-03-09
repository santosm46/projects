function generatePDF(name) { // pode ser passado mais parâmetros
  const doc = new PDFDocument();
  if(doc == null) {
    console.log('error doc null');
    return;
  }
  // pipe the document to a blob
  const stream = doc.pipe(blobStream());
  if(stream == null) {
    console.log('error stream null');
    return;
  }
  let blob;

  // Parte de construção do PDF
  doc.fontSize(25).text('Mensagem: ' + name, 100, 100);

  // fim da construção
  

  // get a blob when you're done
  doc.end();

  const a = document.createElement("a");
  if(a == null) {
    console.log('error a null');
    return;
  }
  document.body.appendChild(a);
  a.style = "display: none";



  stream.on("finish", function() {
    // get a blob you can do whatever you like with
    blob = stream.toBlob("application/pdf");

    // or get a blob URL for display in the browser
    const url = stream.toBlobURL("application/pdf");
    const iframe = document.querySelector("iframe");
    iframe.src = url;
  });

  if (!blob) {
    console.log('error blob null'); // debug
    return;
  }
  var url = window.URL.createObjectURL(blob);
  a.href = url;
  a.download = 'test.pdf';
  a.click();
  window.URL.revokeObjectURL(url);
}