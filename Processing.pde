float ballX, ballY, ballSpeedX, ballSpeedY;
float leftPaddleY, rightPaddleY;
float paddleHeight = 60;
float paddleWidth = 10;
int scorePlayer1 = 0;
int scorePlayer2 = 0;
boolean gameRunning = true;

void setup() {
  size(400, 200);
  ballX = width / 2;
  ballY = height / 2;
  ballSpeedX = 3;
  ballSpeedY = 2;
  leftPaddleY = height / 2;
  rightPaddleY = height / 2;
}

void draw() {
  background(0);
  
  // Display Score
  fill(255);
  textSize(16);
  textAlign(CENTER, CENTER);
  text(scorePlayer1 + " - " + scorePlayer2, width / 2, 20);
  
  if (gameRunning) {
    // Move Ball
    ballX += ballSpeedX;
    ballY += ballSpeedY;

    //Draw ball
    ellipse(ballX, ballY, 10, 10);
    
    // Bounce Ball off Top and Bottom Edges
    if (ballY < 0 || ballY > height) {
      ballSpeedY *= -1;
    }
    
    // Bounce Ball off Paddles
    if (ballX < paddleWidth && ballY > leftPaddleY - paddleHeight / 2 && ballY < leftPaddleY + paddleHeight / 2) {
      ballSpeedX *= -1;
    }
    if (ballX > width - paddleWidth && ballY > rightPaddleY - paddleHeight / 2 && ballY < rightPaddleY + paddleHeight / 2) {
      ballSpeedX *= -1;
    }
    
    // Update Score and Reset Ball if it goes off Left or Right Edge
    if (ballX < 0) {
      scorePlayer2++;
      ballX = width / 2;
      ballY = height / 2;
    }
    if (ballX > width) {
      scorePlayer1++;
      ballX = width / 2;
      ballY = height / 2;
    }
    
    // Check if either player has won
    if (scorePlayer1 >= 10 || scorePlayer2 >= 10) {
      gameRunning = false;
    }
    
    // Move Paddles
    if (keyPressed) {
      if (key == 'w' || key == 'W') {
        leftPaddleY = constrain(leftPaddleY - 5, paddleHeight / 2, height - paddleHeight / 2);
      }
      if (key == 's' || key == 'S') {
        leftPaddleY = constrain(leftPaddleY + 5, paddleHeight / 2, height - paddleHeight / 2);
      }
      if (keyCode == UP) {
        rightPaddleY = constrain(rightPaddleY - 5, paddleHeight / 2, height - paddleHeight / 2);
      }
      if (keyCode == DOWN) {
        rightPaddleY = constrain(rightPaddleY + 5, paddleHeight / 2, height - paddleHeight / 2);
      }
    }
  } else {
    // Display Winning Message
    fill(255);
    textSize(20);
    textAlign(CENTER, CENTER);
    if (scorePlayer1 >= 10) {
      text("PLAYER 1 HAS WON", width / 2, height / 2);
    } else {
      text("PLAYER 2 HAS WON", width / 2, height / 2);
    }
  }
  
  // Draw Paddles
  rect(0, leftPaddleY - paddleHeight / 2, paddleWidth, paddleHeight);
  rect(width - paddleWidth, rightPaddleY - paddleHeight / 2, paddleWidth, paddleHeight);
}
