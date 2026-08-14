let step = 0;
let user = {};

function next(){
 let val = document.getElementById("answer").value;
 if(step==0){ user.name=val; alert("DOB?"); }
 if(step==1){ user.dob=val; alert("Email?"); }
 if(step==2){ user.email=val; alert("Password?"); }
 if(step==3){
   user.password=val;
   fetch("/save_user",{method:"POST",
   headers:{'Content-Type':'application/json'},
   body:JSON.stringify(user)});
   alert("Registered!");
 }
 step++;
}
