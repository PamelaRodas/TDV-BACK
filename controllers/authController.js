const jwt = require('jsonwebtoken');
const { validationResult } = require('express-validator');

const generateToken = (userId) => {
  return jwt.sign({ userId }, process.env.JWT_SECRET, { expiresIn: '30d' });
};

exports.register = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { name, email, password } = req.body;

    if (process.env.DEMO_MODE === 'true') {
      const demoToken = generateToken('demo-user-' + Date.now());
      return res.status(201).json({
        message: 'User registered successfully (DEMO MODE)',
        token: demoToken,
        user: {
          id: 'demo-user-' + Date.now(),
          name: name || 'Demo User',
          email: email || 'demo@example.com',
        },
        demo: true,
      });
    }

    const User = require('../models/User');
    const userExists = await User.findOne({ email });
    if (userExists) {
      return res.status(400).json({ error: 'Email already registered' });
    }

    const user = new User({ name, email, password });
    await user.save();
    const token = generateToken(user._id);

    res.status(201).json({
      message: 'User registered successfully',
      token,
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
      },
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.login = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { email, password } = req.body;

    if (process.env.DEMO_MODE === 'true') {
      const demoToken = generateToken('demo-user-' + Date.now());
      return res.json({
        message: 'Login successful (DEMO MODE)',
        token: demoToken,
        user: {
          id: 'demo-user-' + Date.now(),
          name: email?.split('@')[0] || 'Demo User',
          email: email || 'demo@example.com',
        },
        demo: true,
      });
    }

    const User = require('../models/User');
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const isMatch = await user.comparePassword(password);
    if (!isMatch) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const token = generateToken(user._id);

    res.json({
      message: 'Login successful',
      token,
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
      },
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.validateToken = (req, res) => {
  res.json({
    valid: true,
    user: req.user,
  });
};
