function addSkill() {
  const skillContainer = document.getElementById('skillsContainer');
  const skillDiv = document.createElement('div');
  skillDiv.classList.add('skill-input');

  skillDiv.innerHTML = `
      <input type="text" name="skills[]" placeholder="Skill Name" required>
      <input type="number" name="proficiency[]" min="0" max="100" placeholder="Proficiency (0-100)" required class="proficiency-input">
      <button type="button" onclick="removeSkill(this)">Remove</button>
  `;

  skillContainer.insertBefore(skillDiv, skillContainer.lastElementChild); // Insert before "Add New Skill" card
  updateSkillsHiddenInput(); // Update hidden input after adding a new skill
}

function removeSkill(button) {
  const skillDiv = button.parentElement;
  skillDiv.remove();
  updateSkillsHiddenInput(); // Update hidden input after removing a skill
}

function addProject() {
  const projectContainer = document.getElementById('projectsContainer');
  const projectDiv = document.createElement('div');
  projectDiv.classList.add('project-input');

  projectDiv.innerHTML = `
      <input type="text" name="project_names[]" placeholder="Project Name" required>
      <textarea name="project_descriptions[]" placeholder="Project Description" required></textarea>
      <input type="file" name="project_images[]" accept="image/*" placeholder="Upload Image (optional)">
      <button type="button" onclick="removeProject(this)">Remove</button>
  `;

  projectContainer.insertBefore(projectDiv, projectContainer.lastElementChild); // Insert before "Add New Project" card
  updateProjectsHiddenInput(); // Update hidden input after adding a new project
}

function removeProject(button) {
  const projectDiv = button.parentElement;
  projectDiv.remove();
  updateProjectsHiddenInput(); // Update hidden input after removing a project
}

function editSkill(skillName, proficiency) {
  // Populate the last skill input field with the skill's current data
  const skillInputs = document.querySelectorAll('#skillsContainer .skill-input');
  
  // Find the first empty skill input to populate with edit data
  for (const input of skillInputs) {
      const skillInput = input.querySelector('input[type="text"]');
      const proficiencyInput = input.querySelector('.proficiency-input');

      if (skillInput && proficiencyInput && skillInput.value === '') {
          skillInput.value = skillName;
          proficiencyInput.value = proficiency;
          break; // Stop after filling the first empty field
      }
  }
  updateSkillsHiddenInput(); // Update hidden input after editing a skill
}

function editProject(projectName, projectDescription) {
  // Populate the last project input field with the project's current data
  const projectInputs = document.querySelectorAll('#projectsContainer .project-input');
  
  // Find the first empty project input to populate with edit data
  for (const input of projectInputs) {
      const projectInput = input.querySelector('input[name="project_names[]"]');
      const descriptionInput = input.querySelector('textarea[name="project_descriptions[]"]');

      if (projectInput && descriptionInput && projectInput.value === '') {
          projectInput.value = projectName;
          descriptionInput.value = projectDescription;
          break; // Stop after filling the first empty field
      }
  }
  updateProjectsHiddenInput(); // Update hidden input after editing a project
}

// Function to update the hidden skills input field with current skills
function updateSkillsHiddenInput() {
  const skills = [];
  const skillInputs = document.querySelectorAll('#skillsContainer input[type="text"]');

  skillInputs.forEach(input => {
      if (input.value) {
          skills.push({ name: input.value, proficiency: input.nextElementSibling.value });
      }
  });

  document.getElementById('skills').value = JSON.stringify(skills);
}

// Function to update the hidden projects input fields with current projects
function updateProjectsHiddenInput() {
  const projects = [];
  const projectNames = document.querySelectorAll('#projectsContainer input[name="project_names[]"]');
  const projectDescriptions = document.querySelectorAll('#projectsContainer textarea[name="project_descriptions[]"]');

  projectNames.forEach((input, index) => {
      if (input.value) {
          projects.push({ name: input.value, description: projectDescriptions[index].value });
      }
  });

  document.getElementById('project_names').value = JSON.stringify(projects.map(p => p.name));
  document.getElementById('project_descriptions').value = JSON.stringify(projects.map(p => p.description));
}
