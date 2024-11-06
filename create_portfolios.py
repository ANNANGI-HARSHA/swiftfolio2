import os

# Define the main project directory and portfolio names
project_dir = 'templates'  # Replace with your project directory
portfolio_names = [f'portfolio_{i}' for i in range(1, 6)]

# Loop through each portfolio to create its folders and files
for portfolio in portfolio_names:
    # Create the portfolio folder inside templates
    portfolio_path = os.path.join(project_dir, 'templates', portfolio)
    os.makedirs(portfolio_path, exist_ok=True)

    # Create index.html file
    with open(os.path.join(portfolio_path, 'index.html'), 'w') as f:
        f.write(f'<!DOCTYPE html>\n<html lang="en">\n<head>\n')
        f.write(f'    <meta charset="UTF-8">\n')
        f.write(f'    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write(f'    <link rel="stylesheet" href="css/style.css">\n')
        f.write(f'    <title>{portfolio.replace("_", " ").title()}</title>\n')
        f.write(f'</head>\n<body>\n')
        f.write(f'    <h1>Welcome to {portfolio.replace("_", " ").title()}</h1>\n')
        f.write(f'    <script src="js/script.js"></script>\n')
        f.write(f'</body>\n</html>')

    # Create css directory and style.css file
    css_path = os.path.join(portfolio_path, 'css')
    os.makedirs(css_path, exist_ok=True)
    with open(os.path.join(css_path, 'style.css'), 'w') as f:
        f.write('/* Add your styles here */\n')

    # Create js directory and script.js file
    js_path = os.path.join(portfolio_path, 'js')
    os.makedirs(js_path, exist_ok=True)
    with open(os.path.join(js_path, 'script.js'), 'w') as f:
        f.write('// Add your JavaScript code here\n')

print("Portfolio folders and files created successfully.")
