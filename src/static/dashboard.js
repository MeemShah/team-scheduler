
function toggleForm(formId) {
    document.querySelectorAll("form").forEach(f => f.classList.remove("visible"));
    document.getElementById(formId).classList.add("visible");
    document.getElementById("teamsTable").classList.remove("response-visible");
  }
  
  async function submitGetTeams(e) {
    e.preventDefault();
    const form = e.target;
    const params = new URLSearchParams(new FormData(form)).toString();
    const res = await fetch(`/admin/v1/team/?${params}`);
    const json = await res.json();
  
    if (json.data && Array.isArray(json.data)) {
      const teamsHtml = `
        <h3>Teams List</h3>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Team Name</th>
              <th>Team Lead</th>
              <th>Start Date</th>
            </tr>
          </thead>
          <tbody>
            ${json.data.map(team => `
              <tr>
                <td>${team.id}</td>
                <td>${team.team_name}</td>
                <td>${team.team_lead}</td>
                <td>${team.initial_start_date}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
      const container = document.getElementById("teamsTable");
      container.innerHTML = teamsHtml;
      container.classList.add("response-visible");
    } else {
      document.getElementById("teamsTable").innerHTML = `<p>No teams found or unexpected response.</p>`;
    }
  }
  
  window.onload = async function() {
    const params = new URLSearchParams({
      page: 1,
      limit: 10,
      sort_by: 'id',
      sort_order: 'ASC',
    }).toString();
    const res = await fetch(`/admin/v1/team/?${params}`);
    const json = await res.json();
  
    if (json.data && Array.isArray(json.data)) {
      const teamsHtml = `
        <h3>Teams List</h3>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Team Name</th>
              <th>Team Lead</th>
              <th>Start Date</th>
            </tr>
          </thead>
          <tbody>
            ${json.data.map(team => `
              <tr>
                <td>${team.id}</td>
                <td>${team.team_name}</td>
                <td>${team.team_lead}</td>
                <td>${team.initial_start_date}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
      const container = document.getElementById("teamsTable");
      container.innerHTML = teamsHtml;
      container.classList.add("response-visible");
    } else {
      document.getElementById("teamsTable").innerHTML = `<p>No teams found or unexpected response.</p>`;
    }
  };
  
  async function submitCreateTeam(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const res = await fetch("/admin/v1/team/", {
      method: "POST",
      body: formData
    });
    const msg = await res.text();
    alert(msg);
  }
  
  async function submitAddPairs(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const res = await fetch("/admin/v1/team/team-pairs", {
      method: "POST",
      body: formData
    });
    const msg = await res.text();
    alert(msg);
  }
  