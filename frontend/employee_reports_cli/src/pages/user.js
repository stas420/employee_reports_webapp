// src/pages/User.js
import React from 'react';
import "./user.css";
import { useState } from 'react';
import { registerUsersTime } from '../utils/registrations'
import { useNavigate } from 'react-router-dom';

function User() {

  const [ifStartTime, toggleTimeType] = useState(true);
  const [employeeId, setEmployeeId] = useState('');
  const [workstation, setWorkstation] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  return (
    <div className='user-main-page'>
      <div className='user-header'>
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
                        e.preventDefault();
                        setPassword(e.target.value);
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
                    onClick={() => toggleTimeType(true)}
                />
                <label>
                    start time
                </label>
                <input 
                    type='checkbox'
                    checked={!ifStartTime}
                    onClick={() => toggleTimeType(false)}
                />
                <label>
                    stop time
                </label>
            </div>
      </div>
      <div 
        className='user-submit-button'
        onClick={() => {
            registerUsersTime(employeeId, workstation, password, ifStartTime);
            setEmployeeId('');
            setWorkstation('');
            setPassword('');
            toggleTimeType(true);
        }}
      >
        submit
      </div>
    </div>
  );
}

export default User;
