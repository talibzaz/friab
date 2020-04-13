//IMPLEMENT SHIFT+TAB FUNCTIONALITY WITH SHIFT+ENTER BUTTONS.
let shiftPressed = false; //Variable to check if the the first button is pressed at this exact moment
$(document).keydown(function(e) {
  if (e.shiftKey) { //If it's shift key
    shiftPressed = true; //Set variable to true
  }
}).keyup(function(e) { //If user releases shift button
  if (e.shiftKey) {
    shiftPressed = false; //Set it to false
  }
}); //This way you know if shift key is pressed.

$(document).keydown(function(e) { //For any other keypress event
  if (e.which === 13) { //Checking if it's enter button
    if(shiftPressed === true){ //If it's enter, check if shift key is also pressed
      myFunc(); //Do anything you want
      shiftPressed = false; //Important! Set shiftPressed variable to false. Otherwise the code will work everytime you press the space button again
    }
  }
});
function myFunc() {
   let inputs = $(':input');
   let prevInput = inputs.get(inputs.index(this) - 1);
   if (prevInput) {
      prevInput.focus();
      prevInput.select();
   }
}