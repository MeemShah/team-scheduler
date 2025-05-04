async function callApi(date) {
  const responseElement = document.getElementById('response');
  responseElement.innerHTML = '<p>Loading...</p>';
  document.body.classList.remove('weekend');

  try {
    const res = await fetch(`http://localhost:8000/team/v1/1?query_date=${date}`);
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

    const result = await res.json();
    const { message, data } = result;

    let htmlContent = '';

    if (!data) {
      document.body.classList.add('weekend');
      showConfetti();
    
      htmlContent += `
        <p><strong>Happy weekend! 🎉 🎉 🎉</strong></p>
        <img src="/static/relax.jpg" alt="Weekend Vibes" class="weekend-img" />
      `;
    } else {
      const totalDays = data.total_working_days;
      const scheduledToWork = data.scheduled_to_work.join(', ');
  
      document.title = "Team Schedule";
  
      htmlContent += `
        <div class="team-info-card">
          <h2>${data.team_name}</h2>
          <p><strong>Team Lead:</strong> <span>${data.team_lead}</span></p>
          <p><strong>Scheduled to Work:</strong></p>
          <ul class="schedule-list">
            ${data.scheduled_to_work.map(member => `<li>${member}</li>`).join('')}
          </ul>
          <div class="total-days-highlight">
            <strong>Total Working Days:</strong> ${totalDays}
          </div>
        </div>
      `;
    }

    responseElement.innerHTML = htmlContent;

  } catch (error) {
    responseElement.innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
  }
}

async function getTeamApi(teamId) {
  const membersDiv = document.getElementById("team-members");
  membersDiv.innerHTML = '<p>Loading team members...</p>';

  try {
    const res = await fetch(`http://localhost:8000/team/v1/${teamId}/members`);
    if (!res.ok) throw new Error(`Invalid Team Id! status: ${res.status}`);

    const result = await res.json();
    const { data } = result;

    if (data && data.members.length > 0) {
      let tableHTML = `
        <table>
          <thead>
            <tr>
              <th>Member 1</th>
              <th>Member 2</th>
            </tr>
          </thead>
          <tbody>
            ${data.members.map(pair => `
              <tr>
                <td>${pair[0]}</td>
                <td>${pair[1]}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
      membersDiv.innerHTML = tableHTML;
    } else {
      membersDiv.innerHTML = '<p>No team member pairs found.</p>';
    }

  } catch (error) {
    membersDiv.innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
  }
}

function searchTeam() {
  const dateInput = document.getElementById('dateInput').value;
  if (dateInput) {
    callApi(dateInput);
  } else {
    alert('Please select a date');
  }
}

function showConfetti() {
  const colors = ['#ff6b6b', '#feca57', '#48dbfb', '#1dd1a1', '#5f27cd', '#ff9f43'];

  for (let i = 0; i < 80; i++) {
    const confetti = document.createElement('div');
    confetti.classList.add('confetti');
    confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    confetti.style.left = Math.random() * 100 + 'vw';
    confetti.style.animationDuration = 2 + Math.random() * 3 + 's';
    confetti.style.opacity = Math.random();
    confetti.style.transform = `rotate(${Math.random() * 360}deg)`;
    document.body.appendChild(confetti);

    setTimeout(() => confetti.remove(), 5000);
  }
}

window.onload = () => {
  const today = new Date().toISOString().split('T')[0]; 
  callApi(today);
  getTeamApi(1);
};
