import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { 
    generateAndRequestReport,
    generateAndRequestReportSingleDate
 } from '../utils/adminUtils';
import './styles.css';
import { Helmet } from 'react-helmet-async';
import { getUsersList, updateUser } from '../utils/adminUtils';
import Modal from '../components/modal';

function AdminPanel() {

  const login = useLocation().state?.login;

  const [data, updateData] = useState(getUsersList() || []);
  const [selectedStartDate, selectStartDate] = useState(null);
  const [selectedEndDate, selectEndDate] = useState(null);
  const [ifSingleDate, checkSingleDate] = useState(true);
  const [editingUser, setEditingUser] = useState(null);

  const navigate = useNavigate();

  const handleEdit = (id) => {
    console.log(`Editing ID: ` + id);
    updateData(getUsersList());
    const user = data.find((user) => user.ID === id);
    setEditingUser(user || {});
  };

  const handleSaveUser = (updatedUser) => {
    console.log("user saved UwU" + updatedUser.ID + updatedUser.password);
    
    updateUser(updatedUser);

    updateData((prevData) => {
      return prevData.map((user) => user.ID === updatedUser.ID ? updatedUser : user)
    });

    setEditingUser(null);
  };

  const handleChangePassword = (newPassword) => {
    setEditingUser((prevUser) => ({
      ...prevUser,
      password: newPassword
    }));
  };

  const requestReport = () => {
    if (ifSingleDate) {
        generateAndRequestReportSingleDate("nic");
    }
    else {
        generateAndRequestReport("abc", "def");
    }
  };

  return (
        <div className='main-page'>
          <Helmet>
            <title>admin panel - administration of employees work time and credentials</title>
            <meta name="description" content="admin panel - administration of employees work time and credentials" />
          </Helmet>
          <div className='header'>
            work time administration panel <br/>
            logged as: {login}
            <div 
              className='user-admin-button'
              onClick={() => {
                // log out...
                navigate('/admin');
              }}
            >
                log out
            </div>
          </div>
          <div className='panel-report-section'>
            <div className='panel-report-section-item'>
              {ifSingleDate ? "day of report" : "start date"}
            </div>
            <DatePicker
              selected={selectedStartDate}
              onChange={(date) => {selectStartDate(date);}}
              minDate={new Date(1970, 1, 1)}
              maxDate={new Date()}
              withPortal
            />
            {!ifSingleDate && (
              <div className='panel-report-section-item'>
                end date
              </div>
            )}
            {!ifSingleDate && (
              <DatePicker
                selected={selectedEndDate}
                onChange={(date) => {selectEndDate(date);}}
                minDate={new Date(1970, 1, 1)}
                maxDate={new Date()}
                withPortal
              />
            )}
            <div 
                className='panel-report-download-button'
                onClick={() => {requestReport();}}
            >
                download report
            </div>
            <div className='panel-form-item-input-checkbox'>
                <input 
                    type='checkbox'
                    checked={ifSingleDate}
                    onClick={() => checkSingleDate(true)}
                />
                <label>
                    single-day report
                </label>
                <input 
                    type='checkbox'
                    checked={!ifSingleDate}
                    onClick={() => checkSingleDate(false)}
                />
                <label>
                    date-range report
                </label>
            </div>
          </div>
          <div className='panel-users-section'>
            <div className='panel-users-section-header'>
              <label>
                users database
              </label>
              <div 
                className='panel-users-update-button'
                onClick={() => {updateData(getUsersList() || []);}}
              >
                reload users
              </div>
            </div>
            <table className='panel-users-database-table'>
              <thead>
                <tr>
                  <th>employeeID</th>
                  <th>password</th>
                  <th>edit credentials</th>
                </tr>
              </thead>
              <tbody>
                {data.map(user => (
                  <tr key={user.ID}>
                    <td>{user.ID}</td>
                    <td>***************</td>
                    <td>
                      <button 
                        onClick={() => handleEdit(user.ID)}
                      > 
                        edit 
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
          </table>
          </div>

          <Modal
            show={!!editingUser}
            onClose={() => { setEditingUser(null); }}
            user={editingUser || {}}
            onSave={handleSaveUser}
            onChangePassword={handleChangePassword}
          />

          <div className='admin-bottom-text'>
            in case of any errors, please contact your company's IT support team
          </div>
        </div>
  );
}

export default AdminPanel;
