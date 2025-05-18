async function getSchedule(team_id, query_date) {
  const responseElement = document.getElementById('response');
  const container = document.querySelector('.container');
  responseElement.innerHTML = '<p>Loading...</p>';
  document.body.classList.remove('weekend');

  try {
    const res = await fetch(`/team/v1/${team_id}/schedule?query_date=${query_date}`);
    if (!res.ok) throw new Error(`OOPS!!! Team Id Not Exist`);

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
    const res = await fetch(`/team/v1/${teamId}/details`);
    if (!res.ok) throw new Error(`OOPS!!! Team Id Not Exist`);

    const result = await res.json();
    const { data } = result;

    if (data) {
      const { name, lead, working_days, initial_start_date, pairs } = data;

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
  let dateInput = document.getElementById('dateInput').value;
  const teamIdInput = document.getElementById('teamIdInput').value.trim();
  const searchTerm = document.getElementById('searchTermInput')?.value.trim() || '';

  if (teamIdInput) localStorage.setItem('lastTeamId', teamIdInput);
  if (dateInput) localStorage.setItem('lastDateInput', dateInput);
  localStorage.setItem('lastSearchTerm', searchTerm);

  if (teamIdInput) {
    getTeamInfo(teamIdInput);
    if (!dateInput) {
      dateInput = new Date().toISOString().split('T')[0];
    }
    getSchedule(teamIdInput, dateInput);
  } else if (dateInput) {
    const lastTeamId = localStorage.getItem('lastTeamId') || '1';
    getSchedule(lastTeamId, dateInput);
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
  const savedTeamId = localStorage.getItem('lastTeamId') || '1';
  const savedDate = localStorage.getItem('lastDateInput') || new Date().toISOString().split('T')[0];
  const savedSearchTerm = localStorage.getItem('lastSearchTerm') || '';

  document.getElementById('teamIdInput').value = savedTeamId;
  document.getElementById('dateInput').value = savedDate;
  if (document.getElementById('searchTermInput')) {
    document.getElementById('searchTermInput').value = savedSearchTerm;
  }

  getSchedule(savedTeamId, savedDate);
  getTeamInfo(savedTeamId);
  fetchWeeklySchedule(savedTeamId, savedDate)
};

async function fetchWeeklySchedule(teamId, queryDate) {
  try {
    const response = await fetch(`/team/v1/${teamId}/schedule/week?query_date=${queryDate}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Failed to fetch schedule");
    }

    const container = document.getElementById("schedule-container");
    container.innerHTML = "";

    const table = document.createElement("table");
    table.style.borderCollapse = "collapse";
    table.style.width = "600px";
    table.style.textAlign = "left";

    const headerRow = document.createElement("tr");
    ["Date", "Pair", "Day"].forEach(text => {
      const th = document.createElement("th");
      th.textContent = text;
      th.style.border = "1px solid #ccc";
      th.style.padding = "8px";
      th.style.backgroundColor = "#f2f2f2";
      headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    result.data.forEach(entry => {
      const row = document.createElement("tr");

      const dateCell = document.createElement("td");
      dateCell.textContent = entry.date;
      dateCell.style.border = "1px solid #ccc";
      dateCell.style.padding = "8px";
      
      const pairCell = document.createElement("td");
      pairCell.textContent = Array.isArray(entry.pair)
        ? entry.pair.join(" , ")
        : entry.pair;
      pairCell.style.border = "1px solid #ccc";
      pairCell.style.padding = "8px";

      const dayCell = document.createElement("td");
      dayCell.textContent = entry.day;
      dayCell.style.border = "1px solid #ccc";
      dayCell.style.padding = "8px";


      row.appendChild(dateCell);
      row.appendChild(pairCell);
      row.appendChild(dayCell);
      table.appendChild(row);
    });

    // Add the table to the container
    container.appendChild(table);

  } catch (error) {
    console.error("Error fetching weekly schedule:", error);
    alert("Failed to load schedule.");
  }
}
