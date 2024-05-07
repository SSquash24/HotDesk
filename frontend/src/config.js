const path = "http://localhost:8000/"

module.exports = global.config = {
    api_path: path,

    //GETS
    api_aboutMe: path + "users/me",
    api_myBookings: path + "bookings/me",
    api_todaysBook: path + "bookings/today",
    api_vacancies: path + "bookings/vacancies",
    api_createUser: path + "admin/users/create",

    //POSTS
    api_login: path + "login",
    api_changePassword: path + "users/password",
    api_book: path + "bookings/book",


    today: new Date()

};