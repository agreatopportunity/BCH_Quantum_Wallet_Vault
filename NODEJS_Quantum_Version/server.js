const express = require('express');
const bodyParser = require('body-parser');
const crypto = require('crypto');
const path = require('path');

// mainnet-js is purely ESM, so we must import it dynamically() 
// if we are in a CommonJS file.
let Wallet;

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// --- INITIALIZATION ---
// We wrap server start in an async function to load mainnet-js
async function startServer() {
    try {
        // Dynamic import for ESM-only library
        const mainnet = await import('mainnet-js');
        Wallet = mainnet.Wallet;
        
        app.listen(port, () => {
            console.log(`BCH Quantum Wallet running at http://localhost:${port}`);
        });
    } catch (e) {
        console.error("Failed to load mainnet-js:", e);
    }
}

// --- QUANTUM LIB (Hash Lock Logic) ---

async function createQuantumVault() {
    const secret = crypto.randomBytes(32);
    const secretHash = crypto.createHash('sha256').update(secret).digest();
    
    const scriptBuffer = Buffer.concat([
        Buffer.from('a820', 'hex'),
        secretHash,
        Buffer.from('87', 'hex')
    ]);
    
    const wallet = await Wallet.fromP2SH(scriptBuffer.toString('hex'));
    
    return {
        secret: secret.toString('hex'),
        secretHash: secretHash.toString('hex'),
        address: wallet.address,
        lockingScript: scriptBuffer.toString('hex')
    };
}

// --- API ROUTES ---

app.get('/api/create', async (req, res) => {
    try {
        const vault = await createQuantumVault();
        res.json({ success: true, ...vault });
    } catch (e) {
        res.json({ success: false, error: e.message });
    }
});

app.post('/api/balance', async (req, res) => {
    const { address } = req.body;
    try {
        const wallet = await Wallet.watchOnly(address);
        const balance = await wallet.getBalance('sat');
        res.json({ success: true, balance: balance });
    } catch (e) {
        res.json({ success: false, error: e.message });
    }
});

app.post('/api/sweep', async (req, res) => {
    const { secret, toAddress } = req.body;
    try {
        const secretBuf = Buffer.from(secret, 'hex');
        const secretHash = crypto.createHash('sha256').update(secretBuf).digest();
        const scriptBuffer = Buffer.concat([
            Buffer.from('a820', 'hex'),
            secretHash,
            Buffer.from('87', 'hex')
        ]);
        
        const wallet = await Wallet.fromP2SH(scriptBuffer.toString('hex'));
        
        // Get Balance
        const balance = await wallet.getBalance('sat');
        if (balance < 1000) {
            return res.json({ success: false, error: "Insufficient funds in vault." });
        }
        
        res.json({ 
            success: true, 
            message: "Transaction Constructed (Simulation)",
            txid: "requires_full_node_implementation",
            debug: "Secret verified against hash."
        });
    } catch (e) {
        res.json({ success: false, error: e.message });
    }
});

// Start the app
startServer();
