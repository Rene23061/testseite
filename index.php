<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <script
      src="https://kit.fontawesome.com/1935d064dd.js"
      crossorigin="anonymous"
    ></script>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6"
      crossorigin="anonymous"
    />
    <link rel="stylesheet" href="./css/login.css" />
  </head>
  <body>
    <section class="main">
      <div class="container box">
      <h1 class="text-center">Eule Trading Bots</h1>
        <!-- Login section -->
        <div class="login main-container">
          <div class="login-img img-container">
            <img src="./imc/login-svgrepo-com.svg" alt="login" />
          </div>
          <div class="login-form form-container">
            <form action="login.php" method="post">
              <h2 class="text-center pb-3">Login</h2>
              <input
              name="username"
    type="text"
    class="form-control form-control-lg mb-3"
    placeholder="Username"
              />
              <input
              name="password"
    type="password"
    class="form-control form-control-lg mb-3"
    placeholder="Password"
              />
              <div class="d-grid">
                <button type="submit" class="btn btn-primary btn-lg">Login</button>
              </div>
              <a href="#" class="forgot-link">Forgot password?</a>
              <span>
                Don't have an account?
                <a href="#" class="register-link">Register</a>
              </span>
            </form>
          </div>
        </div>

        <!-- Register section -->
        <div class="register main-container">
          <div class="register-form form-container">
            <form action="">
              <h2 class="text-center pb-3">Register</h2>
              <input
                type="text"
                class="form-control form-control-lg mb-3"
                placeholder="Username"
              />
              <input
                type="email"
                class="form-control form-control-lg mb-3"
                placeholder="Email"
              />
              <input
                type="password"
                class="form-control form-control-lg mb-3"
                placeholder="Password"
              />
              <div class="d-grid">
                <button class="btn btn-primary btn-lg">Register</button>
              </div>

              <span>
                Have an account?
                <a href="#" class="login-link">login</a>
              </span>
            </form>
          </div>
          <div class="register-img img-container">
            <img src="./imc/edit-edit-tools-svgrepo-com.svg" alt="login" />
          </div>
        </div>

        <!-- Forgot section -->
        <div class="forgot main-container">
          <div class="forgot-form form-container">
            <form action="">
              <h2 class="text-center pb-3">Reset Password</h2>

              <input
                type="email"
                class="form-control form-control-lg mb-3"
                placeholder="email"
              />
              <div class="d-grid">
                <button class="btn btn-primary btn-lg">Reset Password</button>
              </div>

              <span> We will send you a reset link!!! </span>
            </form>
            <div class="close">
              <i class="fas fa-times"></i>
            </div>
          </div>
          <div class="forgot-img img-container">
            <img src="./imc/rating-svgrepo-com.svg" alt="forgot" />
          </div>
        </div>
        <div class="footer">
      <p>Automatisiertes Trading mit Tradingview Signal Alarm</p>
    </div>
      </div>
    </section>
    <script src="./js/login.js"></script>
  </body>
</html>
