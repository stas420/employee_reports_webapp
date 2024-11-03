import React from 'react';
import "./styles.css";
import { useState } from 'react';
import { registerUsersTime } from '../utils/registrations'
import { useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';

function User() {

  const [ifStartTime, toggleTimeType] = useState(true);
  const [employeeId, setEmployeeId] = useState('');
  const [workstation, setWorkstation] = useState('');
  const [password, setPassword] = useState('');
  const [registrationFailed, setRegistrationFailed] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);

  const navigate = useNavigate();
  const handleSubmit = () => {
    if (
        employeeId === null || employeeId === '' ||
        workstation === null || workstation === '' ||
        password === null || password === '' ||
        uploadedFile === null
    ) {
        setRegistrationFailed(true);
        return;
    }

    const bool = registerUsersTime(employeeId, workstation, password, ifStartTime);
    
    setRegistrationFailed(bool);

    if (!bool) {
        setEmployeeId('');
        setWorkstation('');
        setPassword('');
        setUploadedFile(null);
        document.getElementById('user-file-input-box').value = '';
        toggleTimeType(true);
    }
  };
  
  return (
    <div className='main-page'>
    <Helmet>
        <title>employee panel - registering work time</title>
        <meta name="description" content="employee panel - registering work time" />
    </Helmet>
      <div className='header'>
        work time registration for employees
        <div 
          className='user-admin-button'
          onClick={() => {navigate('/admin')}}
        >
            admin
        </div>
      </div>
      <div className='user-form'>
            <div className='user-form-item'>
                employee ID
            </div>
            <div className='user-form-item-input'>
                <input 
                    id='user-input-box'
                    value={employeeId}
                    onChange={(e) => {
                        setRegistrationFailed(false);
                        e.preventDefault();
                        setEmployeeId(e.target.value);
                    }}
                >
                </input>
            </div>
            <div className='user-form-item'>
                workstation
            </div>
            <div className='user-form-item-input'>
                <input 
                    id='user-input-box'
                    value={workstation}
                    onChange={(e) => {
                        setRegistrationFailed(false);
                        e.preventDefault();
                        setWorkstation(e.target.value);
                    }}
                >
                </input>
            </div>
            <div className='user-form-item'>
                password
            </div>
            <div className='user-form-item-input'>
                <input 
                    id='user-input-box'
                    type='password'
                    value={password}
                    onChange={(e) => {
                        setRegistrationFailed(false);
                        e.preventDefault();
                        setPassword(e.target.value);
                    }}
                >
                </input>
            </div>
            <div className='user-form-item'>
                your photo
            </div>
            <div className='user-form-item-input'>
                <input 
                    id='user-file-input-box'
                    type='file'
                    accept='image/*'
                    onChange={(e) => {
                        setRegistrationFailed(false);
                        e.preventDefault();
                        const file = e.target.files[0];
                        
                        if (file) {
                            setUploadedFile(file);
                        }
                    }}
                >
                </input>
            </div>

            <div className='user-form-item'>
                registration type:
            </div>
            <div className='user-form-item-input-checkbox'>
                <input 
                    type='checkbox'
                    checked={ifStartTime}
                    onClick={() => {
                        setRegistrationFailed(false);
                        toggleTimeType(true)
                    }}
                />
                <label>
                    start time
                </label>
                <input 
                    type='checkbox'
                    checked={!ifStartTime}
                    onClick={() => {
                        setRegistrationFailed(false);
                        toggleTimeType(false)
                    }}
                />
                <label>
                    stop time
                </label>
            </div>
            <div></div>
            <div>
              <label className='user-failed-register-text'>
                {registrationFailed && (
                    "could not register your data"
                )}
              </label>
            </div>
      </div>
      <div 
        className='user-submit-button'
        onClick={() => {
            handleSubmit();        
        }}
      >
        submit
      </div>
      <div className='user-bottom-text'>
            in case of any problems (for example forgotten password), <br/> please contact your company's IT support team
      </div>
    </div>
  );
}

export default User;
