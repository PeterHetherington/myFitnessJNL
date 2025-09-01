let exerciseCount = 1;

function addExercise() {
  exerciseCount++;
  // get container
  const exerciseFields = document.getElementById("exercise_fields");
  // get element to clone
  const first = document.getElementById("exercise_1");
  // clone the element
  const newdropdown = first.cloneNode(true);
  // update element id
  newdropdown.id = `exercise_${exerciseCount}`;
  newdropdown.className = "";
  // update button attributes
  const button = newdropdown.querySelector("button");
  button.setAttribute("onClick", `removeExercise(${exerciseCount})`);
  button.removeAttribute("hidden");
  // append cloned element to container
  exerciseFields.appendChild(newdropdown);
}

function removeExercise(id) {
  const exerciseField = document.getElementById(`exercise_${id}`);
  exerciseField.remove();
}
