let state = {
    budget: 250000000,
    players: [],
    stats: { matches: 0, wins: 0, draws: 0, losses: 0 }
};

let defaultPlayers = [];
let marketFilter = 'ALL';
let isSimulating = false;
let swapPlayerId = null;

// Initialization
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Obtenim els jugadors "d'internet" (notre JSON generat)
        const response = await fetch('players.json');
        defaultPlayers = await response.json();
    } catch (error) {
        console.error("Error carregant els jugadors d'internet:", error);
    }

    loadState();
    setupNavigation();
    setupMarketFilters();
    document.getElementById('resetBtn').addEventListener('click', resetGame);
    document.getElementById('playMatchBtn').addEventListener('click', simulateMatch);
    updateAll();
});

function loadState() {
    const saved = localStorage.getItem('fcb_president_v2');
    if (saved) {
        state = JSON.parse(saved);
        // Sync new players if any missing in save
        defaultPlayers.forEach(dp => {
            if (!state.players.find(p => p.id === dp.id)) {
                state.players.push({...dp});
            }
        });
    } else {
        state.players = JSON.parse(JSON.stringify(defaultPlayers));
        saveState();
    }
}

function saveState() {
    localStorage.setItem('fcb_president_v2', JSON.stringify(state));
}

function updateAll() {
    renderFinances();
    renderSquad();
    renderLineup();
    renderMarket();
    renderSimulationTab();
}

// FORMATTERS
const formatMoney = (n) => n.toLocaleString() + " €";

// FINANCES
function renderFinances() {
    document.getElementById('budgetDisplay').innerText = formatMoney(state.budget);
    
    const myPlayers = state.players.filter(p => p.inTeam);
    const totalSalaries = myPlayers.reduce((acc, p) => acc + p.salary, 0);
    document.getElementById('salariesDisplay').innerText = "-" + formatMoney(totalSalaries);
}

// NAVIGATION
function setupNavigation() {
    document.querySelectorAll('.menu-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.menu-btn').forEach(b => b.classList.remove('active'));
            e.currentTarget.classList.add('active');
            
            const target = e.currentTarget.getAttribute('data-target');
            document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
            document.getElementById(`view-${target}`).classList.add('active');
        });
    });
}

// SQUAD VIEW
function renderSquad() {
    const myPlayers = state.players.filter(p => p.inTeam);
    document.getElementById('squadCount').innerText = myPlayers.length;
    
    const grid = document.getElementById('squadGrid');
    grid.innerHTML = myPlayers.sort((a,b) => b.rating - a.rating).map(p => `
        <div class="player-card">
            <div class="card-top">
                <span class="card-rating">${p.rating}</span>
                <span class="card-pos pos-${p.position}">${p.position}</span>
            </div>
            <div class="card-body">
                <h3 class="card-name">${p.name}</h3>
                <div class="card-stats-list">
                    <div class="stat-line"><span>Estatus:</span> <strong>${p.status === 'starter' ? 'Titular' : 'Banqueta'}</strong></div>
                    <div class="stat-line"><span>Valor:</span> <strong>${formatMoney(Math.floor(p.price*0.8))}</strong></div>
                    <div class="stat-line"><span>Salari:</span> <strong>${formatMoney(p.salary)}</strong></div>
                </div>
            </div>
            <div class="card-action">
                <button class="btn-action btn-sell" onclick="sellPlayer(${p.id})">Descartar Jugador</button>
            </div>
        </div>
    `).join('');
}

// MARKET VIEW
function setupMarketFilters() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.currentTarget.classList.add('active');
            marketFilter = e.currentTarget.getAttribute('data-pos');
            renderMarket();
        });
    });
}

function renderMarket() {
    let marketPlayers = state.players.filter(p => !p.inTeam);
    if (marketFilter !== 'ALL') {
        marketPlayers = marketPlayers.filter(p => p.position === marketFilter);
    }
    
    const grid = document.getElementById('marketGrid');
    grid.innerHTML = marketPlayers.sort((a,b) => b.rating - a.rating).map(p => {
        const canAfford = state.budget >= p.price;
        return `
        <div class="player-card">
            <div class="card-top">
                <span class="card-rating">${p.rating}</span>
                <span class="card-pos pos-${p.position}">${p.position}</span>
            </div>
            <div class="card-body">
                <h3 class="card-name">${p.name}</h3>
                <div class="card-stats-list">
                    <div class="stat-line"><span>Preu Fixe:</span> <strong>${formatMoney(p.price)}</strong></div>
                    <div class="stat-line"><span>Salari:</span> <strong>${formatMoney(p.salary)}</strong></div>
                </div>
            </div>
            <div class="card-action">
                <button class="btn-action btn-buy ${!canAfford ? 'btn-disabled' : ''}" 
                    onclick="buyPlayer(${p.id})">
                    ${canAfford ? 'Fitxar Jugador' : 'Pressupost Insuficient'}
                </button>
            </div>
        </div>
        `;
    }).join('');
}

// LOGIC ALINEACIO / LINEUP
function renderLineup() {
    const starters = state.players.filter(p => p.inTeam && p.status === 'starter');
    const bench = state.players.filter(p => p.inTeam && p.status === 'bench');
    
    // Validate Lineup
    let errorMsg = '';
    const numPOR = starters.filter(p=>p.position==='POR').length;
    if (starters.length !== 11) errorMsg = `Requerits: 11 / Actuals: ${starters.length}`;
    else if (numPOR !== 1) errorMsg = `Has de tenir exactament 1 porter titular.`;

    const badge = document.getElementById('lineupValidation');
    if (errorMsg) {
        badge.className = 'validation-badge';
        badge.innerText = `⚠️ ${errorMsg}`;
    } else {
        badge.className = 'validation-badge valid';
        badge.innerText = '✅ Alineació vàlida';
    }
    
    // Draw Pitch Rows
    const drawRow = (posId, expectedPos) => {
        document.getElementById(posId).innerHTML = starters
            .filter(p => p.position === expectedPos)
            .map(p => `
                <div class="pitch-player ${swapPlayerId===p.id?'active-swap':''}" onclick="handlePlayerClick(${p.id})">
                    <div class="rating">${p.rating}</div>
                    <div class="name">${p.name.split(' ').pop()}</div>
                </div>
            `).join('');
    };
    
    drawRow('pitch-del', 'DEL');
    drawRow('pitch-mig', 'MIG');
    drawRow('pitch-def', 'DEF');
    drawRow('pitch-por', 'POR');
    
    // Draw Bench
    document.getElementById('benchList').innerHTML = bench.map(p => `
        <div class="bench-item ${swapPlayerId===p.id?'active-swap':''}" onclick="handlePlayerClick(${p.id})">
            <div>
                <span class="card-pos pos-${p.position}">${p.position}</span>
                <strong>${p.name}</strong>
            </div>
            <strong style="color:var(--fcb-gold)">${p.rating}</strong>
        </div>
    `).join('');
}

function handlePlayerClick(id) {
    if (isSimulating) return;
    
    if (swapPlayerId === null) {
        swapPlayerId = id;
    } else {
        if (swapPlayerId !== id) {
            // Swap!
            const p1 = state.players.find(p=>p.id===swapPlayerId);
            const p2 = state.players.find(p=>p.id===id);
            
            // Only swap if one is bench and other is starter
            if (p1.status !== p2.status) {
                const temp = p1.status;
                p1.status = p2.status;
                p2.status = temp;
                saveState();
            }
        }
        swapPlayerId = null;
    }
    renderLineup();
}

// MARKET LOGIC
window.buyPlayer = function(id) {
    const player = state.players.find(p => p.id === id);
    if (!player || player.inTeam) return;
    
    if (state.budget >= player.price) {
        state.budget -= player.price;
        player.inTeam = true;
        player.status = 'bench';
        saveState();
        updateAll();
    }
}

window.sellPlayer = function(id) {
    const player = state.players.find(p => p.id === id);
    if (!player || !player.inTeam) return;
    
    const myPlayers = state.players.filter(p => p.inTeam);
    if (myPlayers.length <= 11) {
        alert("⚠️ No pots vendre. Necessites com a mínim 11 jugadors al club.");
        return;
    }
    if (player.status === 'starter') {
        alert("⚠️ Introdueix aquest jugador a la banqueta abans de vendre'l.");
        return;
    }
    
    state.budget += Math.floor(player.price * 0.8);
    player.inTeam = false;
    player.status = 'none';
    saveState();
    updateAll();
}

// SIMULATION ENGINE
const OPPONENTS = [
    { name: "Reial Madrid", mit: 89 }, { name: "Bayern Múnic", mit: 88 },
    { name: "Manchester City", mit: 89 }, { name: "Arsenal", mit: 86 },
    { name: "Paris SG", mit: 87 }, { name: "Inter Milà", mit: 85 },
    { name: "Liverpool", mit: 87 }, { name: "At. Madrid", mit: 85 },
    { name: "Girona FC", mit: 82 }, { name: "Juventus", mit: 84 }
];

function renderSimulationTab() {
    document.getElementById('statMatches').innerText = state.stats.matches;
    document.getElementById('statWins').innerText = state.stats.wins;
    document.getElementById('statDraws').innerText = state.stats.draws;
    document.getElementById('statLosses').innerText = state.stats.losses;
    
    const starters = state.players.filter(p => p.inTeam && p.status === 'starter');
    let teamMit = 0;
    if (starters.length === 11) {
        teamMit = Math.round(starters.reduce((acc,p)=>acc+p.rating,0)/11);
    }
    document.getElementById('myTeamRating').innerText = `MIT: ${teamMit || '--'}`;
    
    if (!isSimulating && teamMit > 0) {
        const opp = OPPONENTS[state.stats.matches % OPPONENTS.length];
        document.getElementById('opponentTeam').innerHTML = `
            <div class="team-logo dark" style="font-size:1.2rem">${opp.name.substring(0,3).toUpperCase()}</div>
            <div id="oppTeamRating" class="team-rating">MIT: ${opp.mit}</div>
        `;
    }
}

async function simulateMatch() {
    const starters = state.players.filter(p => p.inTeam && p.status === 'starter');
    const numPOR = starters.filter(p=>p.position==='POR').length;
    if (starters.length !== 11 || numPOR !== 1) {
        alert("⚠️ Alineació invàlida. Revisa la pestanya 'L'Alineació'. Has de tenir 11 titulars i exactament 1 porter.");
        return;
    }

    const teamMit = Math.round(starters.reduce((acc,p)=>acc+p.rating,0)/11);
    const opp = OPPONENTS[state.stats.matches % OPPONENTS.length];
    
    // Finance check
    const totalSalaries = state.players.filter(p=>p.inTeam).reduce((acc,p)=>acc+p.salary,0);
    
    isSimulating = true;
    const btn = document.getElementById('playMatchBtn');
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Jugant...`;
    
    const logEl = document.getElementById('matchLog');
    logEl.innerHTML = ``;
    
    const addLog = (msg, cls="") => {
        logEl.innerHTML += `<div class="log-event ${cls}">${msg}</div>`;
        logEl.scrollTop = logEl.scrollHeight;
    };
    
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    
    addLog(`Arbitre xiula l'inici del partit! FC Barcelona vs ${opp.name}`);
    await sleep(800);
    
    let goalsFcb = 0;
    let goalsOpp = 0;
    
    // Quick engine
    for (let min=10; min<=90; min+=15) {
        // Attack FCB
        const attFcb = Math.random() * (teamMit + 5);
        const defOpp = Math.random() * opp.mit;
        if (attFcb > defOpp * 1.1) {
            goalsFcb++;
            const scorer = starters.filter(p=>p.position==='DEL' || p.position==='MIG')[Math.floor(Math.random()*6)] || starters[1];
            addLog(`⏱️ Min ${min}' - GOL DEL BARÇA!! Marca ${scorer.name}! (${goalsFcb}-${goalsOpp})`, "log-goal");
        } else if (attFcb > defOpp * 0.9) {
            addLog(`⏱️ Min ${min}' - Ocasió perillosa pel Barça... s'escapa fregant el pal.`);
        }
        
        await sleep(600);
        
        // Attack Opp
        const attOpp = Math.random() * (opp.mit + 5);
        const defFcb = Math.random() * teamMit;
        if (attOpp > defFcb * 1.1) {
            goalsOpp++;
            addLog(`⏱️ Min ${min+5}' - Gol del ${opp.name}. (${goalsFcb}-${goalsOpp})`, "log-goal");
        }
        
        await sleep(600);
    }
    
    addLog(`🏁 FINAL DEL PARTIT! Resultat: FCB ${goalsFcb} - ${goalsOpp} ${opp.name}`, "log-end");
    
    // Updates
    state.budget -= totalSalaries; // paguem sous
    
    if (goalsFcb > goalsOpp) {
        state.stats.wins++;
        state.budget += 3000000; // Ticket sales + win bonus
        addLog(`💰 Ingressos per Victòria i Entrades: +3,000,000 €`);
    } else if (goalsFcb === goalsOpp) {
        state.stats.draws++;
        state.budget += 1500000;
        addLog(`💰 Ingressos per Empat i Entrades: +1,500,000 €`);
    } else {
        state.stats.losses++;
        state.budget += 800000;
        addLog(`💰 Ingressos per Entrades: +800,000 €`);
    }
    addLog(`💸 Sous pagats a la plantilla: -${formatMoney(totalSalaries)}`);
    
    state.stats.matches++;
    saveState();
    updateAll();
    
    isSimulating = false;
    btn.disabled = false;
    btn.innerHTML = `<i class="fa-solid fa-play"></i> Simular Següent Partit`;
}

function resetGame() {
    if(confirm("⚠️ Aquesta acció esborrarà completament la teva partida actual. Segur?")) {
        localStorage.removeItem('fcb_president_v2');
        location.reload();
    }
}
