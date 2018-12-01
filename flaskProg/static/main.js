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
	var len2 = 0;
	while(true){
		var itemExists = (document.getElementById("purchaseItems-"+len2+"-fruit"));
		if(!itemExists){
			break;
		}
		for(i=0; i<len; i++){
			if(document.getElementById("purchaseItems-"+len2+"-fruit").value == fruitList[i][2]){
				document.getElementById("items-"+i+"-total").value = 
					parseFloat(document.getElementById("purchaseItems-"+len2+"-amount").value)*
					parseFloat(document.getElementById("purchaseItems-"+len2+"-ratio").value)+
					parseFloat(document.getElementById("items-"+i+"-total").value);
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
}