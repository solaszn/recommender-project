
function toggler(){
	var loginbtn = document.getElementById("loginlink");
	var signupbtn = document.getElementById("signuplink");
	var loginfrm = document.querySelector(".login-form");
	var signupfrm = document.querySelector(".register-form");

	// console.log(":)");
	loginbtn.classList.toggle("active");
	signupbtn.classList.toggle("active");
	loginfrm.classList.toggle("x-none");
	signupfrm.classList.toggle("x-none");
}

// ACCOUNTS PAGE

// $(".login-form").velocity("fadeIn", {duration: 1000});


// # use velocity for smooth scroll on landing page
// # use velocity for fadeIn on each form input
// # setup mongo and passport
// # re-learn authentication using node
// # set secret page to dashboard


// alias mongod="C:/Program\ Files/MongoDB/Server/4.2/bin/mongod.exe"
// alias mongo="C:/Program\ Files/MongoDB/Server/4.2/bin/mongo.exe"