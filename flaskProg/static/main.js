function deposit_calc_item(e){
	var cb_id = $(e).attr("id");
	var id_prefix = cb_id.substring(0,cb_id.lastIndexOf("-"));
	var amount = parseFloat(document.getElementById(id_prefix + "-amount").value);
	var ratio = parseFloat(document.getElementById(id_prefix + "-ratio").value);
	var price = parseFloat(document.getElementById(id_prefix + "-price").value);
	var payOut = document.getElementById(id_prefix + "-payOut").checked;
	
	if(!payOut){
		document.getElementById(id_prefix + "-amountLiter").value = Math.floor(amount * ratio / 100);
		document.getElementById(id_prefix + "-amountEuro").value = "0.00";
	}else{
		document.getElementById(id_prefix + "-amountLiter").value = 0;
		document.getElementById(id_prefix + "-amountEuro").value = parseFloat(amount * price / 100).toFixed(2);
	}
	deposit_calc_sum();
}

function deposit_calc_empty_item(e){
	var len = 0;
	var fruitList = [];
	while(true){
		var itemExists = (document.getElementById("items-"+len+"-id"));
		if(!itemExists){
			break;
		}
		entry = [len, 
			document.getElementById("items-"+len+"-id").value,
			document.getElementById("items-"+len+"-name").value,
			document.getElementById("items-"+len+"-ratio").value,
			document.getElementById("items-"+len+"-price").value
			];
		fruitList.push(entry);
		len += 1;
	}
	
	var cb_id = $(e).attr("id");
	var id_prefix = cb_id.substring(0,cb_id.lastIndexOf("-"));
	var boxContent = parseFloat(document.getElementById(id_prefix + "-boxContent").value);
	
	for(i = 0; i<len; i++){
		if(fruitList[i][1] == boxContent){
			document.getElementById(id_prefix + "-ratio").value = fruitList[i][3];
			document.getElementById(id_prefix + "-price").value = fruitList[i][4];
		}
	}
	deposit_calc_item(e);
}

function deposit_calc_sum(){
	var len = 0;
	var fruitList = [];
	while(true){
		var itemExists = (document.getElementById("items-"+len+"-id"));
		if(!itemExists){
			break;
		}
		document.getElementById("items-"+len+"-amount").value = 0;
		document.getElementById("items-"+len+"-total").value = 0;
		entry = [len, 
			document.getElementById("items-"+len+"-id").value,
			document.getElementById("items-"+len+"-name").value,
			document.getElementById("items-"+len+"-amount").value
			];
		fruitList.push(entry);
		len += 1;
	}
	var len2 = 0;
	while(true){
		var itemExists = (document.getElementById("depositItems-"+len2+"-boxContent"));
		if(!itemExists){
			break;
		}
		for(i=0; i<len; i++){
			if(document.getElementById("depositItems-"+len2+"-boxContent").value == fruitList[i][2]){
				document.getElementById("items-"+i+"-amount").value = 
					parseFloat(document.getElementById("depositItems-"+len2+"-amount").value)+
					parseFloat(document.getElementById("items-"+i+"-amount").value);
				document.getElementById("items-"+i+"-total").value = 
					parseFloat(document.getElementById("depositItems-"+len2+"-amountLiter").value)+
					parseFloat(document.getElementById("items-"+i+"-total").value);
			}
			if(i == len-1){
				document.getElementById("items-"+i+"-amount").value = "-";
				document.getElementById("items-"+i+"-total").value = 
					parseFloat(document.getElementById("items-"+i+"-total").value) + 
					parseFloat(document.getElementById("depositItems-"+len2+"-amountEuro").value);
				document.getElementById("items-"+i+"-total").value = parseFloat(document.getElementById("items-"+i+"-total").value).toFixed(2);
			}
		}
		len2 += 1;
	}
	var len3 = 0;
	while(true){
		var itemExists = (document.getElementById("emptyDepositItems-"+len3+"-boxContent"));
		if(!itemExists){
			break;
		}
		for(i=0; i<len; i++){
			if(document.getElementById("emptyDepositItems-"+len3+"-boxContent").value == fruitList[i][1]){
				document.getElementById("items-"+i+"-amount").value = 
					parseFloat(document.getElementById("emptyDepositItems-"+len3+"-amount").value)+
					parseFloat(document.getElementById("items-"+i+"-amount").value);
				document.getElementById("items-"+i+"-total").value = 
					parseFloat(document.getElementById("emptyDepositItems-"+len3+"-amountLiter").value)+
					parseFloat(document.getElementById("items-"+i+"-total").value);
			}
			if(i == len-1){
				document.getElementById("items-"+i+"-amount").value = "-";
				document.getElementById("items-"+i+"-total").value = 
					parseFloat(document.getElementById("items-"+i+"-total").value) + 
					parseFloat(document.getElementById("emptyDepositItems-"+len3+"-amountEuro").value);
				document.getElementById("items-"+i+"-total").value = parseFloat(document.getElementById("items-"+i+"-total").value).toFixed(2);
			}
		}
		len3 += 1;
	}
}

function purchase_calc_item(e){
	var cb_id = $(e).attr("id");
	var id_prefix = cb_id.substring(0,cb_id.lastIndexOf("-"));
	var amount = parseFloat(document.getElementById(id_prefix + "-amount").value);
	var price = parseFloat(document.getElementById(id_prefix + "-price").value);

	document.getElementById(id_prefix + "-total").value = parseFloat(amount * price).toFixed(2);
	
	purchase_calc_sum();
}

function purchase_calc_sum(){
	var len = 0;
	var fruitList = [];
	while(true){
		var itemExists = (document.getElementById("items-"+len+"-id"));
		if(!itemExists){
			break;
		}
		document.getElementById("items-"+len+"-total").value = 0;
		entry = [len, 
			document.getElementById("items-"+len+"-id").value,
			document.getElementById("items-"+len+"-name").value,
			];
		fruitList.push(entry);
		len += 1;
	}
	
	var depListLen = 0;
	var depositList = [];
	while(true){
		var itemExists = (document.getElementById("customerDeposits-"+depListLen+"-fruit"));
		if(!itemExists){
			break;
		}
		entry = [depListLen, 
			document.getElementById("customerDeposits-"+depListLen+"-fruit").value,
			parseFloat(document.getElementById("customerDeposits-"+depListLen+"-amount").value),
			0
			];
		depositList.push(entry);
		depListLen += 1;
	}
	
	var len2 = 0;
	while(true){	//jeden Artikel durchgehen
		var itemExists = (document.getElementById("purchaseItems-"+len2+"-fruit"));
		if(!itemExists){
			break;
		}
		for(i=0; i<len; i++){	//jede Frucht durchgehen
			if(document.getElementById("purchaseItems-"+len2+"-fruit").value == fruitList[i][2]){
				document.getElementById("items-"+i+"-total").value = 
					parseFloat(document.getElementById("purchaseItems-"+len2+"-amount").value)*
					parseFloat(document.getElementById("purchaseItems-"+len2+"-ratio").value)+
					parseFloat(document.getElementById("items-"+i+"-total").value);
			}
			if(i<depListLen && document.getElementById("purchaseItems-"+len2+"-fruit").value == depositList[i][1]){
				depositList[i][3] += parseFloat(document.getElementById("purchaseItems-"+len2+"-amount").value);
			}
			if(i == len-1){
				document.getElementById("items-"+i+"-total").value = 
					parseFloat(document.getElementById("items-"+i+"-total").value) + 
					parseFloat(document.getElementById("purchaseItems-"+len2+"-total").value);
				document.getElementById("items-"+i+"-total").value = parseFloat(document.getElementById("items-"+i+"-total").value).toFixed(2);
			}
		}
		len2 += 1;
	}
	var compListLen = 0;
	var compensationList = [];
	var compSum = 0;
	while(true){
		var itemExists = (document.getElementById("purchaseCompensations-"+compListLen+"-fruitName"));
		if(!itemExists){
			break;
		}
		entry = [compListLen, 
			document.getElementById("purchaseCompensations-"+compListLen+"-fruitName").value,
			parseFloat(document.getElementById("purchaseCompensations-"+compListLen+"-amount").value),
			0
			];
		compensationList.push(entry);
		for(i=0; i<depListLen; i++){
			if(document.getElementById("purchaseCompensations-"+compListLen+"-fruitName").value == depositList[i][1]){
				document.getElementById("purchaseCompensations-"+compListLen+"-amount").value = Math.max(0,depositList[i][3]-depositList[i][2])
				document.getElementById("purchaseCompensations-"+compListLen+"-total").value = 
					Math.max(0,depositList[i][3]-depositList[i][2])*
					parseFloat(document.getElementById("purchaseCompensations-"+compListLen+"-price").value);
				compSum += parseFloat(document.getElementById("purchaseCompensations-"+compListLen+"-total").value);
			}
		}
		compListLen += 1;
	}
	
	document.getElementById("items-"+(len-1)+"-total").value = 
		parseFloat(document.getElementById("items-"+(len-1)+"-total").value) + 
		compSum;
	document.getElementById("items-"+(len-1)+"-total").value = parseFloat(document.getElementById("items-"+(len-1)+"-total").value).toFixed(2);
}