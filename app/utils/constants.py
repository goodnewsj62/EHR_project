EMAIL_TEMPLATE = lambda url, name: """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    /* General styles for the email */
    body {
      font-family: Arial, sans-serif;
      background-color: #f9f9f9;
      margin: 0;
      padding: 0;
    }
    .email-container {
      max-width: 600px;
      margin: 20px auto;
      background-color: #ffffff;
      border: 1px solid #ddd;
      border-radius: 5px;
      padding: 20px;
    }
    .email-header {
      text-align: center;
      padding-bottom: 20px;
    }
    .email-header h1 {
      font-size: 24px;
      color: #333;
    }
    .email-content {
      font-size: 16px;
      color: #555;
      line-height: 1.5;
    }
    .email-button {
      display: inline-block;
      margin: 20px 0;
      padding: 10px 20px;
      background-color: #007BFF;
      color: #ffffff;
      text-decoration: none;
      border-radius: 5px;
      font-size: 16px;
    }
    .email-footer {
      text-align: center;
      font-size: 12px;
      color: #999;
      padding-top: 20px;
    }
  </style>
</head>
<body>
  <div class="email-container">
    <div class="email-header">
      <h1>Activate Your Account</h1>
    </div>
    <div class="email-content">
      <p>Hi "${replace-name}",</p>
      <p>Thank you for registering with EHR App. To activate your account, please click the button below:</p>
      <p style="text-align: center;">
        <a href="${replace-url}" class="email-button">Activate My Account</a>
      </p>
      <p>If you didn’t register for this account, you can safely ignore this email.</p>
    </div>
    <div class="email-footer">
      <p>&copy; 2025 EHR App. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
""".replace(
    "${replace-name}", name
).replace(
    "${replace-url}", url
)
