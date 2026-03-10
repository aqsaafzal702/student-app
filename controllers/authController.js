const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const User = require('../models/User');

// Show Signup Page
const getSignup = (req, res) => {
    res.render('auth/signup');
};

// Handle Signup
const postSignup = async (req, res) => {
    try {
        const { username, email, password } = req.body;

        // Check if user already exists
        const existingUser = await User.findOne({ where: { email } });
        if (existingUser) {
            req.flash('error_msg', 'Email already registered!');
            return res.redirect('/auth/signup');
        }

        // Hash password
        const hashedPassword = await bcrypt.hash(password, 10);

        // Create user
        await User.create({ username, email, password: hashedPassword });

        req.flash('success_msg', 'Signup successful! Please login.');
        res.redirect('/auth/login');

    } catch (error) {
        console.log(error);
        req.flash('error_msg', 'Something went wrong!');
        res.redirect('/auth/signup');
    }
};

// Show Login Page
const getLogin = (req, res) => {
    res.render('auth/login');
};

// Handle Login
const postLogin = async (req, res) => {
    try {
        const { email, password } = req.body;

        // Check if user exists
        const user = await User.findOne({ where: { email } });
        if (!user) {
            req.flash('error_msg', 'Email not registered!');
            return res.redirect('/auth/login');
        }

        // Check password
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            req.flash('error_msg', 'Wrong password!');
            return res.redirect('/auth/login');
        }

        // Set session
        req.session.user = { id: user.id, username: user.username, email: user.email };
        res.redirect('/students');

    } catch (error) {
        console.log(error);
        req.flash('error_msg', 'Something went wrong!');
        res.redirect('/auth/login');
    }
};

// Handle Logout
const logout = (req, res) => {
    req.session.destroy();
    res.redirect('/auth/login');
};

module.exports = { getSignup, postSignup, getLogin, postLogin, logout };