async function callApi() {
    console.log("script.js loaded");

    const responseElement = document.getElementById('response');
    responseElement.innerHTML = 'Loading...';
    document.body.classList.remove('weekend');
  
    try {
      const res = await fetch('https://team-scheduler-4.onrender.com/team-pair/today');
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
  
      const result = await res.json();
      const { message, data } = result;
  
      const teamMembers = data.team_member.map(name => `<li>${name}</li>`).join('');
      const totalDays = data.total_working_days;
  
      responseElement.innerHTML = `
        <p><strong>Message:</strong> ${message}</p>
        <p><strong>Total Working Days:</strong> ${totalDays}</p>
        <p><strong>Team Members:</strong></p>
        <ul>${teamMembers}</ul>
      `;
  
      if (message === "Happy Weekend") {
        document.body.classList.add('weekend');
        showConfetti();
      }
  
    } catch (error) {
      responseElement.innerHTML = 'Error: ' + error.message;
    }
  }
  
  function showConfetti() {
    for (let i = 0; i < 100; i++) {
      const confetti = document.createElement('div');
      confetti.textContent = '🎉';
      confetti.style.position = 'fixed';
      confetti.style.left = Math.random() * 100 + 'vw';
      confetti.style.top = Math.random() * 100 + 'vh';
      confetti.style.fontSize = Math.random() * 24 + 16 + 'px';
      confetti.style.animation = 'fall 3s linear forwards';
      document.body.appendChild(confetti);
  
      setTimeout(() => confetti.remove(), 3000);
    }
  }
  