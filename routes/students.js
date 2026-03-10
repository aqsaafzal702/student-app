const express = require('express');
const router = express.Router();
const { getAllStudents, getAddStudent, postAddStudent, getEditStudent, postEditStudent, deleteStudent } = require('../controllers/studentController');

// Auth Middleware
const isAuth = (req, res, next) => {
    if (req.session.user) {
        next();
    } else {
        req.flash('error_msg', 'Please login first!');
        res.redirect('/auth/login');
    }
};

router.get('/', isAuth, getAllStudents);
router.get('/add', isAuth, getAddStudent);
router.post('/add', isAuth, postAddStudent);
router.get('/edit/:id', isAuth, getEditStudent);
router.post('/edit/:id', isAuth, postEditStudent);
router.delete('/delete/:id', isAuth, deleteStudent);

module.exports = router;