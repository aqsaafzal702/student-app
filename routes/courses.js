const express = require('express');
const router = express.Router();
const { getAllCourses, getAddCourse, postAddCourse, getEditCourse, postEditCourse, deleteCourse } = require('../controllers/courseController');

// Auth Middleware
const isAuth = (req, res, next) => {
    if (req.session.user) {
        next();
    } else {
        req.flash('error_msg', 'Please login first!');
        res.redirect('/auth/login');
    }
};

router.get('/', isAuth, getAllCourses);
router.get('/add', isAuth, getAddCourse);
router.post('/add', isAuth, postAddCourse);
router.get('/edit/:id', isAuth, getEditCourse);
router.post('/edit/:id', isAuth, postEditCourse);
router.delete('/delete/:id', isAuth, deleteCourse);

module.exports = router;