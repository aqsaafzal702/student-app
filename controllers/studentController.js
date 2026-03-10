const Student = require('../models/Student');

// Get All Students
const getAllStudents = async (req, res) => {
    try {
        const students = await Student.findAll();
        res.render('students/index', { students });
    } catch (error) {
        console.log(error);
        req.flash('error_msg', 'Something went wrong!');
        res.redirect('/');
    }
};

// Show Add Student Form
const getAddStudent = (req, res) => {
    res.render('students/add');
};

// Handle Add Student
const postAddStudent = async (req, res) => {
    try {
        const { name, email, phone, address } = req.body;
        await Student.create({ name, email, phone, address });
        req.flash('success_msg', 'Student added successfully!');
        res.redirect('/students');
    } catch (error) {
        console.log(error);
        req.flash('error_msg', 'Something went wrong!');
        res.redirect('/students/add');
    }
};

// Show Edit Student Form
const getEditStudent = async (req, res) => {
    try {
        const student = await Student.findByPk(req.params.id);
        res.render('students/edit', { student });
    } catch (error) {
        console.log(error);
        req.flash('error_msg', 'Something went wrong!');
        res.redirect('/students');
    }
};

// Handle Edit Student
const postEditStudent = async (req, res) => {
    try {
        const { name, email, phone, address } = req.body;
        await Student.update(
            { name, email, phone, address },
            { where: { id: req.params.id } }
        );
        req.flash('success_msg', 'Student updated successfully!');
        res.redirect('/students');
    } catch (error) {
        console.log(error);
        req.flash('error_msg', 'Something went wrong!');
        res.redirect('/students');
    }
};

// Handle Delete Student
const deleteStudent = async (req, res) => {
    try {
        await Student.destroy({ where: { id: req.params.id } });
        req.flash('success_msg', 'Student deleted successfully!');
        res.redirect('/students');
    } catch (error) {
        console.log(error);
        req.flash('error_msg', 'Something went wrong!');
        res.redirect('/students');
    }
};

module.exports = { getAllStudents, getAddStudent, postAddStudent, getEditStudent, postEditStudent, deleteStudent };