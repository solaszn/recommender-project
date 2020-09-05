function generate(){
	$(".col-md-4").addClass("d-none");
	var ind_selects = document.getElementById("opt-industries");
	var srvc_selects = document.getElementById("opt-services");

	var industry = ind_selects.options[ind_selects.selectedIndex].value;
	var company = srvc_selects.options[srvc_selects.selectedIndex].value;
	eel.recommend(industry, company, 5)(pasteRecommendations)
}

function pasteRecommendations(data){
	console.log(typeof(data))
	var name = document.getElementById("name").value;
	document.getElementById("company-name").textContent = String(name);
	// document.getElementById("paste").textContent = String(data);
	var appdata = ["behance","facebook","github","instagram","linkedin","medium","pinterest","reddit","research-gate","snapchat","spotify","tiktok","tumblr","twitter","youtube"];
	for (var i = 0; i <= 4; i++) {
	    for (var j = 0; j < appdata.length; j++){
	        if (appdata[j] == data[i]){
	            $("#"+appdata[j]).removeClass("d-none");
	            console.log(data[i], appdata[j]);
	        }
	    }
	}
}
