<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eule Media Loader</title>
    <link rel="stylesheet" href="css/loader-home.css">
</head>
<script>
    setTimeout(function(){
        window.location.href = 'home1.php';
    }, 3000);
</script>
<div class="loader">
<body><div class="loader1">
Willkommen 
</div>
    <svg
			class="gooey-filter"
			width="0"
			height="0"
			xmlns="http://www.w3.org/2000/svg"
			version="1.1">
			<defs>
				<filter id="goo">
					<feGaussianBlur
						in="SourceGraphic"
						stdDeviation="12"
						result="blur" />
					<feColorMatrix
						in="blur"
						mode="matrix"
						values="1  0  0  0  0
							0  1  0  0  0
							0  0  1  0  0
							0  0  0  25  -12"
						result="goo" />
					<feComposite in="SourceGraphic" in2="goo" operator="atop" />
				</filter>
			</defs>
		</svg>

		<div class="loader">
			<div class="static">
				<div class="dot"></div>
				<div class="dot"></div>
				<div class="dot"></div>
				<div class="dot"></div>
			</div>
			<div class="dots">
				<div class="dot animated"></div>
				<div class="dot"></div>
				<div class="dot"></div>
				<div class="dot"></div>
				<div class="dot"></div>
			</div>
		</div>
		<div class="loader2 ">
    die Seite wird geladen...
    </div>
	</div>
  </body>
</html>