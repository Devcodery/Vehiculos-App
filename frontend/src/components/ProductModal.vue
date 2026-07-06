<template>
  <Transition name="modal-fade">
    <div class="modal-overlay" @click.self="cerrar">
      <div class="modal-content cell-shaded">
        
        <header class="modal-header">
          <h2 class="modal-title"><i class="fa-solid fa-box-open"></i> REGISTRAR PRODUCTO</h2>
          <button @click="cerrar" class="close-btn"><i class="fa-solid fa-xmark"></i></button>
        </header>
        
        <form @submit.prevent="saveProduct" class="comic-form">
          <div class="form-grid">
            <div class="input-group">
              <label for="marca_prod" class="label-form">Marca:</label>
              <input id="marca_prod" v-model="productForm.marca" type="text" class="input-form" required placeholder="Ej: Castrol">
            </div>

            <div class="input-group">
              <label for="nombre_prod" class="label-form">Nombre:</label>
              <input id="nombre_prod" v-model="productForm.nombre" type="text" class="input-form" required placeholder="Ej: Aceite Sintético 5W-30">
            </div>

            <div class="input-group">
              <label for="referencia_prod" class="label-form">Referencia / Código:</label>
              <input id="referencia_prod" v-model="productForm.referencia" type="text" class="input-form" placeholder="Ej: BR-9902">
            </div>

            <div class="input-group">
              <label for="categoria_prod" class="label-form">Categoría:</label>
              <select id="categoria_prod" v-model="productForm.categoria" class="input-form select-form" required>
                <option value="" disabled>Selecciona una categoría...</option>
                <option value="Aceites y Fluidos">Aceites y Fluidos</option>
                <option value="Filtros">Filtros</option>
                <option value="Frenos">Frenos</option>
                <option value="Motor y Escape">Motor y Escape</option>
                <option value="Suspensión y Dirección">Suspensión y Dirección</option>
                <option value="Baterías y Electricidad">Baterías y Electricidad</option>
                <option value="Neumáticos y Llantas">Neumáticos y Llantas</option>
                <option value="Herramientas y Consumibles">Herramientas y Consumibles</option>
                <option value="Otras Piezas">Otras Piezas</option>
              </select>
            </div>

            <div class="input-group" style="grid-column: 1 / -1;">
              <label for="detalles_prod" class="label-form">Detalles (Opcional):</label>
              <textarea id="detalles_prod" v-model="productForm.detalles" rows="3" class="input-form" placeholder="Especificaciones, cantidad, compatibilidad..."></textarea>
            </div>
          </div>

          <div class="input-group upload-group">
            <label for="imagen_prod" class="label-form">Imagen del Producto:</label>
            <input id="imagen_prod" type="file" @change="handleFileUpload" accept="image
.input-group {
    display: grid;
    margin: 0.5em;
}

label, .label-form {
    color: #00e5ff !important;
    font-family: 'Bangers', cursive !important;
    font-size: 1.2rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    margin: 0.35em;
}

.input-form, .file-input, .select-form {
    padding: 10px 12px !important;
    background: #000 !important;
    color: #ffffff !important;
    border: 2px solid #fff !important;
    outline: none !important;
    transition: border-color 0.2s ease;
    width: 100%;
    box-sizing: border-box;
    font-family: 'Orbitron', sans-serif !important;
}

.input-form:focus, .file-input:focus, .select-form:focus {
    border-color: #00e5ff !important;
}


textarea.input-form {
    resize: vertical;
    box-sizing: border-box;
    font-family: 'Orbitron', sans-serif !important;
}
</style>