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
      const teamMembers = data.members.map(pair => `
          <tr>
              <td>${pair[0]}</td>
              <td>${pair[1]}</td>
          </tr>
      `).join('');
  
      const totalDays = data.total_working_days;
      const scheduledToWork = data.scheduled_to_work.join(', ');
  
      document.title = "Team Schedule";
  
      htmlContent += `
          <div class="team-info">
              <p><strong>Team Name:</strong> ${data.team_name}</p>
              <p><strong>Team Lead:</strong> ${data.team_lead}</p>
              <p><strong>Scheduled to Work:</strong> ${scheduledToWork}</p>
              <div class="total-days">
                  <strong>Total Working Days:</strong> ${totalDays}
              </div>
          </div>
          
          <div class="team-members-table">
              <h3>Team Members Pairs:</h3>
              <table>
                  <thead>
                      <tr>
                          <th>Member 1</th>
                          <th>Member 2</th>
                      </tr>
                  </thead>
                  <tbody>
                      ${teamMembers}
                  </tbody>
              </table>
          </div>
      `;
  }
  

    responseElement.innerHTML = htmlContent;

  } catch (error) {
    responseElement.innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
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
};
