inAuthPage=function(){
  if(window.location.pathname.startsWith("/auth/") && !window.location.pathname.startsWith("/auth/reset") ){
    console.log("in auth page");
    return true
  }
  else{
    console.log("Not in auth page");
    return false
  }
}
$(".goToFor").on("click", function(){
  if(inAuthPage()){
  $('#carousel-1').carousel(0)}
  else{
    window.document.location="/auth"
  }
});
$(".goToLogin").on("click", function(){
  if(inAuthPage()){
    $('#carousel-1').carousel(1)}
    else{
      window.document.location="/auth/login"
    }});
$(".goToReg").on("click", function(){
  if(inAuthPage()){
    $('#carousel-1').carousel(2)}
    else{
      window.document.location="/auth/register"
    }});
// $(document).ready(function(){
//     $('#carousel-1').carousel(1)});

