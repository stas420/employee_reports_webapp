import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { 
    generateAndRequestReport,
    generateAndRequestReportSingleDate
 } from '../utils/adminUtils';
import './styles.css';

function AdminPanel({ login }) {

  const [selectedDate, selectDate] = useState(null);
  const [ifSingleDate, checkSingleDate] = useState(true);
  const navigate = useNavigate();

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
          <div className='header'>
            work time administration panel
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
              heloł
            </div>
            <DatePicker
              selected={selectedDate}
              onChange={(date) => {selectDate(date);}}
              minDate={new Date(1970, 1, 1)}
              maxDate={new Date()}
            />
            <div 
                className='panel-report-download-button'
                onClick={() => {requestReport();}}
            >
                download report
            </div>
          </div>
          <div className='panel-users-section'>
              <label>
                here you will manage users
              </label>
          </div>
          <div className='admin-bottom-text'>
            in case of any errors, please contact your company's IT support team
          </div>
        </div>
  );
}

export default AdminPanel;
