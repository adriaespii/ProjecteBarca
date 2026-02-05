# 📑 Planificació del Projecte: Simulador de President del FC Barcelona

## 1. Anàlisi Inicial del Projecte
En aquesta fase es defineix l'abast, els objectius i l'estructura del treball per garantir l'èxit del desenvolupament.

### 📌 1.1 Definició del Projecte
* **Objectiu principal:** Desenvolupar una aplicació web interactiva per gestionar la plantilla, l'economia i la simulació de partits del FC Barcelona.
* **Usuaris objectiu:** Aficionats al futbol i seguidors interessats en la gestió esportiva.
* **Tecnologies:** HTML5, CSS3, JavaScript ES6 i `localStorage`.
* **Requisits visuals:** Disseny *Responsive* i colors corporatius blaugrana.

### 📌 1.2 Identificació de Mòduls (Transversalitat DAW/DAM)
* **Llenguatges de Marques (LLMM):** Estructura i estils (HTML/CSS).
* **Entorns de Desenvolupament (ED):** Control de versions amb Git/GitHub.
* **Programació (PR):** Lògica del joc amb JavaScript (Arrays, JSON, funcions).
* **Bases de Dades (BD):** Disseny de model de dades per a la persistència.

---

## 2. Gestió amb Trello / ClickUp (Metodologia Kanban)
L'organització del treball es divideix en llistes que representen el flux de treball i les àrees clau del producte.

### 🗂️ Llista 1: Gestió General (Project Management)
* **[Targeta] Anàlisi de Requisits (Fet ✅)**
    * Definir RF (Funcionals) i RNF (No funcionals).
* **[Targeta] Maquetació i Estructura (En curs 🏃)**
    * Crear Dashboard.html amb CSS Grid.
    * Implementar disseny responsive.
* **[Targeta] Algorisme de Simulació (Pendent ✏️)**
    * Crear funció `simularPartit()` amb factor aleatori.

### 🗂️ Llista 2: Desenvolupament del Producte (Product Backlog)
* **[Targeta] Lògica del Mercat de Fitxatges**
    * Crear array de jugadors disponibles.
    * Validar saldo abans de cada compra.
* **[Targeta] Disseny de Fitxa de Jugador (Card UI)**
    * Crear la visualització tipus "carta" amb dades i mitjana.
* **[Targeta] Persistència de Dades**
    * Guardar l'estat del club a `localStorage`.

### 🗂️ Llista 3: Màrqueting i Creixement
* **[Targeta] Campanya #JoSócPresident**
    * Estratègia de difusió en xarxes socials i fòrums.
* **[Targeta] Tutorial d'Usuari**
    * Crear guia visual de com no arribar a la fallida econòmica.

---

## 3. Fites i Lliurables (Milestones)

| Fita | Descripció | Lliurable | Estat |
| :--- | :--- | :--- | :--- |
| **Fita 1** | Anàlisi i Requisits | Document de Requisits | Completat ✅ |
| **Fita 2** | Disseny i Arquitectura | Mockups i Wireframes | En curs 🟡 |
| **Fita 3** | Estructura Web | Codi Frontend (HTML/CSS) | Pendent ⚪ |
| **Fita 4** | Lògica i Funcionalitat | Beta funcional (JS) | Pendent ⚪ |
| **Fita 5** | Lliurament Final | Projecte desplegat + Memòria | Pendent ⚪ |

---

## 4. R+D+I (Recerca i Desenvolupament)
Funcionalitats avançades per a futures versions:
* **PWA:** Investigar com fer l'app instal·lable al mòbil.
* **APIs Externes:** Connectar amb dades reals de La Lliga.
* **Animacions:** Millorar l'experiència amb la llibreria GSAP.

---

## 5. Restriccions i Recursos
* **Temps:** 3-4 setmanes lectives.
* **Software:** Visual Studio Code, Git, Chrome DevTools.
* **Limitació tècnica:** No s'utilitza base de dades externa (tot resideix al client).