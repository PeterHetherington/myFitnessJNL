function addSet(exerciseId) {
  // find correct element
  const sets = document.getElementById(`extraSets_${exerciseId}`);

  // find new set number
  const setCount = sets.children.length + 2;

  // add new set
  const div = document.createElement("div");
  div.className = "row log-sets";
  div.id = `set_${setCount}_${exerciseId}`;
  div.innerHTML = `
    <div class="col-auto">
      <input type="hidden" name="exercise_id"  value="${exerciseId}">
      <input type="hidden" name="set_num"  value="${setCount}">
      <label class="col-form-label">Set ${setCount}</label>
    </div>
    <div class="col">
      <input class="form-control" type="number" name="weight" placeholder="Weight">
    </div>
    <div class="col">
      <input class="form-control" type="number" name="reps" placeholder="Reps">
    </div> 
        `;
  sets.appendChild(div);
}

function removeSet(exerciseId) {
  // find correct element
  const sets = document.getElementById(`extraSets_${exerciseId}`);

  // check if there is a set to remove
  if (sets.children.length > 0) {
    // ensure the user can only remove last set in order to not break set count
    sets.removeChild(sets.lastChild);
  }
}
