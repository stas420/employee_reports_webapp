import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { adminLogIn } from '../utils/adminUtils';
import { Helmet } from 'react-helmet-async';
import './styles.css';

function Admin() {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const [loginFailed, setLoginFailed] = useState(false);

  const navigate = useNavigate();

  const handleLogIn = () =>{
    const bool = adminLogIn(login, password);

    if (bool) {
        navigate('/admin/panel', { state : { login } });
    }
    else {
        setLoginFailed(true);
    }
  };

  return (
        <div className='main-page'>
          <Helmet>
            <title>admin panel login - administration of employees work time and credentials</title>
            <meta name="description" content="admin panel login - administration of employees work time and credentials" />
          </Helmet>
          <div className='header'>
            work time administration panel - login
            <div 
              className='user-admin-button'
              onClick={() => {navigate('/user')}}
            >
                employee
            </div>
          </div>
          <div className='admin-form'>
                <div 
                  className='user-form-item'
                >
                    login
                </div>
                <div className='user-form-item-input'>
                    <input 
                        id='user-input-box'
                        value={login}
                        onChange={(e) => {
                          setLoginFailed(false);
                          e.preventDefault();
                          setLogin(e.target.value);
                        }}      
                    >
                    </input>
                </div>
                <div 
                  className='user-form-item'
                  type='password'
                >
                    password
                </div>
                <div className='user-form-item-input'>
                    <input 
                        id='user-input-box'
                        type='password'
                        value={password}
                        onChange={(e) => {
                          setLoginFailed(false);
                          e.preventDefault();
                          setPassword(e.target.value);
                        }}      
                    >
                    </input>
                </div>
                <div></div>
                <div className='admin-failed-login-text'>
                    <label>
                        {loginFailed ? "log-in failed, try again please" : ""}
                    </label>
                </div>
          </div>
          <div 
            className='admin-login-button'
            onClick={() => {
                handleLogIn();
            }}
          >
            log in
          </div>
          <div className='admin-bottom-text'>
            in case of any errors, please contact your company's IT support team
          </div>
        </div>
  );
}

export default Admin;
