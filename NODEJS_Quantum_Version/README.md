# Node.js Cryptocurrency Wallet

A lightweight web-based cryptocurrency wallet built with Node.js, Express, and mainnet-js.

> ⚠️ **Important**: This project requires **mainnet-js version 1.0.0** specifically. Please ensure you install the correct version using `npm install mainnet-js@1.0.0`

## 🚀 Quick Start

```bash
# Clone the repository (or create project folder)
mkdir my-wallet && cd my-wallet

# Install dependencies (Note: mainnet-js v1.0.0 specifically required)
npm install express mainnet-js@1.0.0 body-parser cors

# Start the server
node server.js

# Open in browser
# Navigate to: http://localhost:3000
```

## 📋 Prerequisites

- **Node.js**: v22.17.1 or higher (check with `node --version`)
- **npm**: Comes with Node.js (check with `npm --version`)

## 🛠️ Installation

### Step 1: Project Setup

You have two options to initialize the project:

#### Option A: Use Provided Configuration (Recommended)
If you have the provided `package.json` file, simply place it in your project folder.

#### Option B: Initialize New Project
```bash
npm init -y
```
This creates a default `package.json` file.

### Step 2: Install Dependencies

Install all required packages:

```bash
npm install express mainnet-js@1.0.0 body-parser cors
```

**Important**: We specifically use `mainnet-js@1.0.0` for compatibility.

This command will:
- Create a `node_modules` folder
- Install the following packages:
  - **express**: Web application framework
  - **mainnet-js@1.0.0**: Cryptocurrency operations library (version 1.0.0)
  - **body-parser**: Parse incoming request bodies
  - **cors**: Enable Cross-Origin Resource Sharing

#### Alternative: Install packages individually

```bash
npm install express
npm install mainnet-js@1.0.0
npm install body-parser
npm install cors
```

### Step 3: Project Structure

Ensure your project has the following structure:

```
my-wallet/
├── server.js           # Main server file
├── package.json        # Project configuration
├── package-lock.json   # Dependency lock file (auto-generated)
├── node_modules/       # Dependencies (auto-generated)
└── public/            # Frontend files
    ├── index.html     # Main HTML file
    ├── app.js         # Frontend JavaScript
    └── style.css      # Stylesheet
```

### Step 4: Create Required Files

Create the following files in your project:

1. **server.js** - Main server application
2. **public/index.html** - Wallet interface
3. **public/app.js** - Frontend logic
4. **public/style.css** - Styling

## 🚦 Running the Application

### Start the Server

```bash
node server.js
```

You should see a message like:
```
Server running on http://localhost:3000
```

### Access the Wallet

Open your web browser and navigate to:
```
http://localhost:3000
```

## 📦 Package Information

### Dependencies

| Package | Version | Description |
|---------|---------|-------------|
| express | latest | Fast, unopinionated web framework |
| mainnet-js | **1.0.0** | JavaScript library for cryptocurrency operations |
| body-parser | latest | Node.js body parsing middleware |
| cors | latest | Enable CORS with various options |

⚠️ **Version Note**: This project specifically requires `mainnet-js@1.0.0`. Using a different version may cause compatibility issues.

### Sample package.json

```json
{
  "name": "my-wallet",
  "version": "1.0.0",
  "description": "A simple cryptocurrency wallet",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.0",
    "mainnet-js": "1.0.0",
    "body-parser": "^1.20.0",
    "cors": "^2.8.5"
  },
  "keywords": ["wallet", "cryptocurrency", "nodejs"],
  "author": "",
  "license": "MIT"
}
```

**Note**: The `mainnet-js` version is pinned to `1.0.0` for compatibility.

## 🔧 Configuration

### Server Configuration

The server runs on port 3000 by default. To change this, modify the port in `server.js`:

```javascript
const PORT = process.env.PORT || 3000;
```

### CORS Configuration

CORS is enabled by default. Modify CORS settings in `server.js` if needed:

```javascript
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}));
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
**Error**: `EADDRINUSE: address already in use :::3000`

**Solution**: 
- Kill the process using port 3000, or
- Change the port in server.js

```bash
# Find process using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>
```

#### 2. Module Not Found
**Error**: `Cannot find module 'express'`

**Solution**: Reinstall dependencies
```bash
rm -rf node_modules package-lock.json
npm install
```

#### 3. Permission Denied
**Error**: `EACCES: permission denied`

**Solution**: Run with proper permissions
```bash
sudo npm install
```

#### 4. Wrong mainnet-js Version
**Error**: `TypeError` or unexpected behavior with mainnet-js functions

**Solution**: Ensure you have version 1.0.0 installed
```bash
# Check installed version
npm list mainnet-js

# If wrong version, uninstall and reinstall
npm uninstall mainnet-js
npm install mainnet-js@1.0.0
```

## 📝 Development

### Running in Development Mode

For automatic server restart on file changes, install nodemon:

```bash
npm install --save-dev nodemon
```

Then add to `package.json` scripts:
```json
"scripts": {
  "start": "node server.js",
  "dev": "nodemon server.js"
}
```

Run development server:
```bash
npm run dev
```

## 🔒 Security Considerations

⚠️ **Important**: This is a basic wallet implementation. For production use:

- Never expose private keys in the frontend
- Use HTTPS in production
- Implement proper authentication
- Store sensitive data securely
- Use environment variables for configuration
- Implement rate limiting
- Add input validation and sanitization

## 📚 API Endpoints

The server provides the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Serve wallet interface |
| POST | /api/wallet/create | Create new wallet |
| GET | /api/wallet/balance | Get wallet balance |
| POST | /api/wallet/send | Send transaction |

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Check the [Troubleshooting](#-troubleshooting) section
- Open an issue on GitHub
- Consult the mainnet-js documentation: [mainnet.cash](https://mainnet.cash/)

## 🔗 Resources

- [Node.js Documentation](https://nodejs.org/docs/)
- [Express.js Guide](https://expressjs.com/guide)
- [mainnet-js Documentation](https://mainnet.cash/docs/)
- [MDN Web Docs](https://developer.mozilla.org/)

---

**Note**: Always backup your wallet data and never share your private keys!
