import React from 'react';
import './modal.css';

const Modal = ({ show, onClose, user, onSave, onChangePassword }) => {
  if (!show) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>edit selected employee</h2>
        <div className='modal-edit-section-grid'>
          <div>
            <label className='modal-label'>
              employeeID:
            </label>
            <input 
              className='modal-input'
              type="text" 
              value={user.ID}
              readOnly
            />
          </div>
          <div>
            <label
              className='modal-label'
            >
              password:
            </label>
            <input
              //type='password'
              className='modal-input'
              value={user.password}
              onChange={(e) => { onChangePassword(e.target.value); }}
            />
          </div>
        </div>
        <div className='modal-button-section'>
          <div 
            onClick={onClose}
            className='modal-button'
          >
            cancel
          </div>
          <div
            onClick={() => onSave(user)}
            className='modal-button'
          >
            save changes
          </div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
