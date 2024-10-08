// const path = "http://localhost:8000/"
const path = "/api/"

module.exports = global.config = {
    api_path: path,

    //GETS
    api_aboutMe: path + "users/me",
    api_myBookings: path + "bookings/me",
    api_todaysBook: path + "bookings/today",
    api_vacancies: path + "bookings/vacancies",
    api_createUser: path + "admin/users/create",
    api_img: path + "plans/1/image",
    api_seat: path + "seats/me",
    api_colleages: path + "seats/dept",

    //POSTS
    api_login: path + "login",
    api_changePassword: path + "users/password",
    api_book: path + "bookings/book",


    today: new Date()

};