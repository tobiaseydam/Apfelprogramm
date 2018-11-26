function deposit_addLine(){
	var tableRef = document.getElementById('depositItems').getElementsByTagName('tbody')[0];
	var newRow   = tableRef.insertRow(tableRef.rows.length);
	
	var newPosCell  = newRow.insertCell(0);
	var newPosText  = document.createTextNode(tableRef.rows.length-1)
	newPosCell.appendChild(newPosText);
	
	var newBoxCell  = newRow.insertCell(1);
	var newBoxDiv = document.createElement("DIV");
	newBoxCell.appendChild(newBoxDiv);
	var newBoxInput = document.createElement("SELECT");
	newBoxDiv.appendChild(newBoxInput);
	
	var newContentCell  = newRow.insertCell(2);
	var newContentDiv = document.createElement("DIV");
	newContentCell.appendChild(newContentDiv);
	var newContentText = document.createTextNode("Kisteninhalt");
	newContentDiv.appendChild(newContentText);
	
	var newAmountCell  = newRow.insertCell(3);
	var newAmountDiv = document.createElement("DIV");
	newAmountCell.appendChild(newAmountDiv);
	var newAmountInput = document.createElement("INPUT");
	newAmountDiv.appendChild(newAmountInput);
}