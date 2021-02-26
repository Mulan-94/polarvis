<!DOCTYPE html>
<html>
<head>
  <title>403 Forbidden</title>
  <meta name="author" content="mulan-94">
  <meta charset="utf-8">
  <link href="https://fonts.googleapis.com/css?family=Bangers" rel="stylesheet">
  <style>
    html{
        width: 100%;
        height: 100%;
    }
    body {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      border: 20px dashed rgba(255, 192, 203, 0.678);
      font-family: "Bangers";
      max-height: 93vh;
      min-height: 93vh;
      ver
    }
    h1 {
        font-size: 100px;
    }
    p {
        font-size: 50px;
    }
    span {
      background-color: rgba(255, 0, 0, 0.342);
    }
  </style>
</head>
<body>
  <h1> Door Number <span>  404 </span>: Not Found</h1>
  <p>The requested URL or file:
      <span style="background-color: #d3f5f9; font-family: monospace; font-size: 50px;">

        <?php
            echo $_SERVER["REQUEST_URI"];
        ?> 
      </span>was not found on this server &#128551
  </p>
</body>
</html>