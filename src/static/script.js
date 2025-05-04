async function getSchedule(query_date) {
  const responseElement = document.getElementById('response');
  const container = document.querySelector('.container');
  responseElement.innerHTML = '<p>Loading...</p>';
  document.body.classList.remove('weekend');

  try {
    const res = await fetch(`https://team-scheduler-4.onrender.com/team/v1/1/schedule?query_date=${query_date}`);
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

    const result = await res.json();
    const { data } = result;

    let htmlContent = '';

    if (!data) {
      document.body.classList.add('weekend');
      container.style.backgroundSize = 'cover';
      container.style.backgroundPosition = 'center';
      container.style.backgroundRepeat = 'no-repeat';
      showConfetti();

      htmlContent = `
        <div class="weekend-card">
          <p><strong>Happy weekend! 🎉 🎉 🎉</strong></p>
          <img src="/static/relax.jpg" alt="Weekend Vibes" class="weekend-img" />
        </div>
      `;
    } else {
      container.style.backgroundSize = 'cover';
      container.style.backgroundPosition = 'center';
      container.style.backgroundRepeat = 'no-repeat';

      const totalDays = data.total_working_days;
      const scheduledToWork = data.scheduled_to_work || [];

      document.title = "Team Schedule";

      htmlContent = `
        <div class="team-info-card">
          <h2>Today's Schedule</h2>
          <ul>
            ${scheduledToWork.map(member => `<li>${member}</li>`).join('')}
          </ul>
          <div class="total-days">
            <strong>Total Working Days:</strong> ${totalDays}
          </div>
        </div>
      `;
    }

    responseElement.innerHTML = htmlContent;

  } catch (error) {
    responseElement.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
  }
}


async function getTeamInfo(teamId) {
  const membersDiv = document.getElementById("team-members");
  membersDiv.innerHTML = '<p>Loading team members...</p>';

  try {
    const res = await fetch(`https://team-scheduler-4.onrender.com/team/v1/${teamId}/details`);
    if (!res.ok) throw new Error(`Invalid Team Id! status: ${res.status}`);

    const result = await res.json();
    const { data } = result;

    if (data) {
      const { name, lead, initial_start_date, pairs } = data;

      let tableHTML = `
        <div class="team-header">
          <p><strong>Team:</strong> ${name}</p>
          <p><strong>Lead:</strong> ${lead}</p>
          <p><strong>Start Date:</strong> ${initial_start_date}</p>
        </div>
      `;

      if (pairs && pairs.length > 0) {
        tableHTML += `
          <table>
            <thead>
              <tr>
                <th>Member 1</th>
                <th>Member 2</th>
              </tr>
            </thead>
            <tbody>
              ${pairs.map(pair => `
                <tr>
                  <td>${pair[0]}</td>
                  <td>${pair[1]}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        `;
      } else {
        tableHTML += '<p>No team member pairs found.</p>';
      }

      membersDiv.innerHTML = tableHTML;
    } else {
      membersDiv.innerHTML = '<p>Team data not found.</p>';
    }

  } catch (error) {
    membersDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
  }
}

function searchTeam() {
  const dateInput = document.getElementById('dateInput').value;
  if (dateInput) {
    getSchedule(dateInput);
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
  getSchedule(today);
  getTeamInfo(1);
};
