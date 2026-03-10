const Course = require('../models/Course');

// Get All Courses
const getAllCourses = async (req, res) => {
    try {
        const courses = await Course.findAll();
        res.render('courses/index', { courses });
    } catch (error) {
        console.log(error);
        req.flash('error_msg', 'Something went wrong!');
        res.redirect('/');
    }
};

// Show Add Course Form
const getAddCourse = (req, res) => {
    res.render('courses/add');
};

// Handle Add Course
const postAddCourse = async (req, res) => {
    try {
        const { name, code, credits, description } = req.body;
        await Course.create({ name, code, credits, description });
        req.flash('success_msg', 'Course added successfully!');
        res.redirect('/courses');
    } catch (error) {
        console.log(error);
        req.flash('error_msg', 'Something went wrong!');
        res.redirect('/courses/add');
    }
};

// Show Edit Course Form
const getEditCourse = async (req, res) => {
    try {
        const course = await Course.findByPk(req.params.id);
        res.render('courses/edit', { course });
    } catch (error) {
        console.log(error);
        req.flash('error_msg', 'Something went wrong!');
        res.redirect('/courses');
    }
};

// Handle Edit Course
const postEditCourse = async (req, res) => {
    try {
        const { name, code, credits, description } = req.body;
        await Course.update(
            { name, code, credits, description },
            { where: { id: req.params.id } }
        );
        req.flash('success_msg', 'Course updated successfully!');
        res.redirect('/courses');
    } catch (error) {
        console.log(error);
        req.flash('error_msg', 'Something went wrong!');
        res.redirect('/courses');
    }
};

// Handle Delete Course
const deleteCourse = async (req, res) => {
    try {
        await Course.destroy({ where: { id: req.params.id } });
        req.flash('success_msg', 'Course deleted successfully!');
        res.redirect('/courses');
    } catch (error) {
        console.log(error);
        req.flash('error_msg', 'Something went wrong!');
        res.redirect('/courses');
    }
};

module.exports = { getAllCourses, getAddCourse, postAddCourse, getEditCourse, postEditCourse, deleteCourse };