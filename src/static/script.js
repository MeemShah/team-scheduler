async function callApi(date = 'today') {
  const responseElement = document.getElementById('response');
  responseElement.innerHTML = '<p>Loading...</p>';
  document.body.classList.remove('weekend');

  try {
    const res = await fetch(`https://team-scheduler-4.onrender.com/team-pair/${date}`);
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
      const teamMembers = data.team_member.map(name => `<li>${name}</li>`).join('');
      const totalDays = data.total_working_days;

      document.title = "Bkash Schedule For Team";

      htmlContent += `
        <p><strong>Team Unstoppable:</strong></p>
        <div class="team-members-container">
          <ul>${teamMembers}</ul>
        </div>
        <div class="total-days">
          <strong>Total Working Days:</strong> ${totalDays}
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

window.onload = () => callApi(); 
