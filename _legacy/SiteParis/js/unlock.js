 function Translate() { 
    //initialization
    this.init =  function(attribute, lng){
        this.attribute = attribute;
        this.lng = lng;    
    }
    //translate 
    this.process = function(){
                _self = this;
                var xrhFile = new XMLHttpRequest();
                //load content data 
                xrhFile.open("GET", "./languages/"+this.lng+".json", false);
                xrhFile.onreadystatechange = function ()
                {
                    if(xrhFile.readyState === 4)
                    {
                        if(xrhFile.status === 200 || xrhFile.status == 0)
                        {
                            var LngObject = JSON.parse(xrhFile.responseText);
                            console.log(LngObject["name1"]);
                            var allDom = document.getElementsByTagName("*");
                            for(var i =0; i < allDom.length; i++){
                                var elem = allDom[i];
                                var key = elem.getAttribute(_self.attribute);
                                 
                                if(key != null) {
                                    if(key == "theorder-contact-name" || key == "theorder-contact-email" || key == "theorder-contact-phone"|| key == "theorder-contact-message"){
                                        //Exception Translate contact form
                                        if(key == "theorder-contact-name")
                                            elem.placeholder = LngObject["theorder-contact-name"];
                                        else if (key == "theorder-contact-email")
                                            elem.placeholder = LngObject["theorder-contact-email"];
                                        else if (key == "theorder-contact-phone")
                                            elem.placeholder = LngObject["theorder-contact-phone"];
                                        else if (key == "theorder-contact-message")
                                            elem.placeholder = LngObject["theorder-contact-message"];
                                        /* TODO correct this whe in Python
                                        elem["data-validation-required-message"] = LngObject["theorder-contact-name-error"];
                                        $("#name").attr("data-validation-required-message",LngObject["theorder-contact-name-error"]);
                                        */
                                    } else {
                                        //console.log(key);
                                        elem.innerHTML = LngObject[key]  ;
                                    }
                                }

                            }


                     
                        }
                    }
                }
                xrhFile.send();
    }    
}

$( document ).ready(function() {

    var translate = new Translate();
    var lang = window.location.search.substr(6,2)
    var currentLng = lang;//'fr' ou en
    //Default language
    if (currentLng == "")
        currentLng = 'en';

	//lang link
	if(lang == "fr") {
		$("#button-lang").attr("href", "?lang=en");
	} else {
		$("#button-lang").attr("href", "?lang=fr");
	}
	
    var attributeName = 'data-tag';
    translate.init(attributeName, currentLng);
    translate.process(); 

});
