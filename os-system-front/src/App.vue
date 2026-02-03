<template>
  <div class="main-layout">
    <router-view />
  </div>
</template>

<style>
* {
  box-sizing: border-box;
}

body, html {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background-color: #f0f2f5;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

#app {
  height: 100%;
}

.main-layout {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.page-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 100px 20px 40px;
  background-color: #f0f2f5;
}


.base-card {
  background-color: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  width: 100%;
}


.auth-size {
  max-width: 400px;
}


.content-size {
  max-width: 800px;
}

h2, h1 {
  margin-top: 0;
  color: #2c3e50;
  text-align: center;
  margin-bottom: 25px;
}

</style>
