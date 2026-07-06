<template>
    <div class="dashboard-wrapper">
        <header class="section-header cell-shaded">
            <h2 class="section-title">
                <i class="fa-solid fa-car-side"></i> EXPEDIENTE: {{ formulario.alias || formulario.matricula ||
                'CARGANDO...' }}
            </h2>
        </header>

        <div v-if="cargando" class="loading-state">
            <i class="fa-solid fa-circle-notch fa-spin"></i> Cargando telemetría...
        </div>

        <div v-else class="grid-2-col">

            <section class="car-profile cell-shaded">
                <div class="image-container">
                    <img v-if="formulario.imagen" :src="getImagenUrl(formulario.imagen)" alt="Foto del vehículo"
                        class="car-photo" />
                    <div v-else class="no-photo">
                        <i class="fa-solid fa-camera-retro"></i>
                        <p>SIN FOTO REGISTRADA</p>
                    </div>
                </div>

                <form @submit.prevent="guardarCambios" class="comic-form">
                    <div class="input-group">
                        <label>MATRÍCULA</label>
                        <input type="text" v-model="formulario.matricula" class="brutalist-input disabled-input"
                            disabled />
                    </div>

                    <div class="two-fields">
                        <div class="input-group">
                            <label>MARCA</label>
                            <input type="text" v-model="formulario.marca" class="brutalist-input" required />
                        </div>
                        <div class="input-group">
                            <label>MODELO</label>
                            <input type="text" v-model="formulario.modelo" class="brutalist-input" required />
                        </div>
                    </div>

                    <div class="two-fields">
                        <div class="input-group">
                            <label>ALIAS (Opcional)</label>
                            <input type="text" v-model="formulario.alias" class="brutalist-input" />
                        </div>
                        <div class="input-group">
                            <label>KILOMETRAJE ACTUAL</label>
                            <input type="number" v-model.number="formulario.kilometraje" class="brutalist-input"
                                required />
                        </div>
                    </div>

                    <div class="input-group upload-group">
                        <label for="foto_vehiculo" class="label-form">Subir nueva foto:</label>
                        <input id="foto_vehiculo" type="file" @change="handleFileUpload" accept="image
.section-header {
    background: var(--panel-bg, #111);
    padding: 15px 20px;
    border: 4px solid #fff;
    margin-bottom: 30px;
}

.section-title {
    font-family: 'Bangers', cursive;
    font-size: 2.5rem;
    color: #00ff66;
    margin: 0;
    letter-spacing: 2px;
}

.loading-state {
    text-align: center;
    color: #00e5ff;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.5rem;
    padding: 50px;
}


.grid-2-col {
    display: grid;
    grid-template-columns: 1fr 1.2fr;
    gap: 30px;
}

@media (max-width: 900px) {
    .grid-2-col {
        grid-template-columns: 1fr;
    }
}


.car-profile {
    background: #111;
    border: 4px solid #ff00ff;
    padding: 25px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    box-shadow: 12px 12px 0 #000;
}

.image-container {
    width: 100%;
    height: 250px;
    border: 3px dashed #555;
    background: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}

.car-photo {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.no-photo {
    text-align: center;
    color: #555;
    font-family: 'Bangers', cursive;
    font-size: 1.2rem;
}

.no-photo i {
    font-size: 3rem;
    margin-bottom: 10px;
    color: #333;
}


.comic-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.two-fields {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.input-group {
    display: flex;
    flex-direction: column;
    margin: 0;
}

label,
.label-form {
    color: #00e5ff !important;
    font-family: 'Bangers', cursive !important;
    font-size: 1.2rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    margin-bottom: 5px;
}

.brutalist-input,
.file-input {
    width: 100%;
    padding: 10px 12px;
    background: #000;
    color: #fff;
    border: 2px solid #fff;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1rem;
    outline: none;
    box-sizing: border-box;
    transition: border-color 0.2s;
}

.brutalist-input:focus,
.file-input:focus {
    border-color: #00e5ff;
}

.disabled-input {
    background: #222;
    color: #888;
    border-color: #444;
    cursor: not-allowed;
}

.file-input {
    cursor: pointer;
}

.save-btn {
    background: #ff00ff !important;
    color: #000 !important;
    font-family: 'Bangers', cursive;
    font-size: 1.5rem;
    padding: 12px;
    border: 3px solid #000;
    cursor: pointer;
    margin-top: 10px;
    transition: transform 0.1s;
}

.save-btn:hover:not(:disabled) {
    transform: translate(-3px, -3px);
    box-shadow: 4px 4px 0 #000;
}

.save-btn:disabled {
    background: #555;
    cursor: not-allowed;
}

.mensaje-alerta {
    padding: 10px;
    font-family: 'Orbitron', sans-serif;
    font-weight: bold;
    text-align: center;
    border: 2px solid #000;
    margin-top: 10px;
}

.exito {
    background: #00ff66;
    color: #000;
}

.error {
    background: #ff3333;
    color: #fff;
}


.telemetry-panel {
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.stat-box {
    background: #111;
    padding: 20px;
    border: 4px solid #fff;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    
}

.money-box {
    border-color: #00ff66;
    box-shadow: 8px 8px 0 rgba(0, 255, 102, 0.3);
}

.stat-icon {
    font-size: 2.5rem;
    margin-bottom: 10px;
}

.money-box .stat-icon {
    color: #00ff66;
}

.stat-box h4 {
    color: #fff;
    font-family: 'Bangers', cursive;
    font-size: 1.3rem;
    margin: 0 0 10px 0;
    letter-spacing: 1px;
}

.stat-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.2rem;
    font-weight: bold;
    color: #fff;
    margin-bottom: 5px;
}

.money-box .stat-value {
    color: #00ff66;
}

.stat-subtext {
    color: #888;
    font-family: 'Roboto', sans-serif;
    font-size: 0.85rem;
    margin: 0;
    font-style: italic;
}


.next-maintenance-panel {
    background: #111;
    border: 4px solid #ffcc00;
    box-shadow: 8px 8px 0 rgba(255, 204, 0, 0.3);
    padding: 20px;
}

.panel-title {
    color: #ffcc00;
    font-family: 'Bangers', cursive;
    font-size: 1.8rem;
    margin: 0 0 15px 0;
    border-bottom: 2px dashed #444;
    padding-bottom: 10px;
}

.maintenance-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
    max-height: 250px;
    overflow-y: auto;
    padding-right: 5px;
}

.maintenance-list::-webkit-scrollbar {
    width: 6px;
}

.maintenance-list::-webkit-scrollbar-thumb {
    background: #ffcc00;
}

.maintenance-item {
    background: #000;
    border: 2px solid #555;
    padding: 12px;
}

.maintenance-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.maintenance-name {
    color: #fff;
    font-family: 'Bangers', cursive;
    font-size: 1.3rem;
    letter-spacing: 1px;
}

.maintenance-status-badge {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.75rem;
    font-weight: bold;
    padding: 3px 8px;
    border: 1px solid #000;
}

.status-al-dia {
    background: #00ff66;
    color: #000;
}

.status-proximo {
    background: #ffcc00;
    color: #000;
}

.status-vencido {
    background: #ff3366;
    color: #fff;
}

.maintenance-details p {
    margin: 4px 0;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.85rem;
    color: #ccc;
}

.maintenance-details strong {
    color: #00e5ff;
}

.never-done {
    color: #ff3366 !important;
    font-style: italic;
}

.last-done {
    color: #888 !important;
}

.empty-maintenance {
    text-align: center;
    color: #666;
    padding: 20px;
    font-family: 'Orbitron', sans-serif;
}

.empty-maintenance i {
    font-size: 2rem;
    margin-bottom: 10px;
    display: block;
}


.history-list {
    background: #111;
    border: 4px solid #ff00ff;
    padding: 20px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    box-shadow: 8px 8px 0 rgba(255, 0, 255, 0.3);
}

.history-title {
    color: #ff00ff;
    font-family: 'Bangers', cursive;
    font-size: 1.8rem;
    margin: 0 0 20px 0;
    border-bottom: 2px dashed #444;
    padding-bottom: 10px;
}

.services-wrapper {
    display: flex;
    flex-direction: column;
    gap: 15px;
    overflow-y: auto;
    max-height: 400px;
    padding-right: 5px;
}

.services-wrapper::-webkit-scrollbar {
    width: 6px;
}

.services-wrapper::-webkit-scrollbar-thumb {
    background: #ff00ff;
}


.brutalist-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Orbitron', sans-serif;
    color: #fff;
    background: #000;
    border: 2px solid #555;
}

.brutalist-table th,
.brutalist-table td {
    border: 1px solid #333;
    padding: 10px;
    text-align: left;
}

.brutalist-table th {
    background: #222;
    color: #ff00ff;
    font-family: 'Bangers', cursive;
    font-size: 1.1rem;
    letter-spacing: 1px;
}

.table-km {
    color: #00e5ff;
    font-weight: bold;
}

.table-price {
    color: #00ff66;
    font-weight: bold;
}

.table-notes {
    font-family: 'Roboto', sans-serif;
    color: #aaa;
    font-style: italic;
    font-size: 0.9rem;
}

.empty-history {
    text-align: center;
    color: #666;
    padding: 30px;
    font-family: 'Orbitron', sans-serif;
}

.empty-history i {
    font-size: 2.5rem;
    color: #444;
    margin-bottom: 10px;
    display: block;
}
</style>