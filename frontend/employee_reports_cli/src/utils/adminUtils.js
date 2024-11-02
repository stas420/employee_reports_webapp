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