export function adminLogIn(login, password) {
    return (String(login) === "admin" && String(password) === "admin"); 
}

export function generateAndRequestReportSingleDate(singleDate) {
    console.log("generateAndRequestReport called "
        + singleDate
    );
}

export function generateAndRequestReport(dateFrom, dateTo) {
    console.log("generateAndRequestReport called "
        + dateFrom + " " + dateTo
    );
};

export function getUsersList() {

    // fetching users will be done here

    const user1 = {
        ID: "bobson",
        password: String(12345)
    };

    const user2 = {
        ID: "aleksander",
        password: "brzykcy"
    };

    const user3 = {
        ID: "robert",
        password: "lewandoski"
    };

    const userArray = [user1, user2];

    return userArray;
}