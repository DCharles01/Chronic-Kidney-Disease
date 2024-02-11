import React, { useState } from 'react';
import './MyForm.css';

const MyForm = () => {
  const [formData, setFormData] = useState({
    age: 0,
    bloodPressure: 0,
    redBloodCellCount: 0,
    whiteBloodCellCount: 0,
    packedCellVolume: 0,
    serumCreatinine: 0,
    sodium: 0,
    potassium: 0,
    hemoglobin: 0,
    redBloodCells: 'normal',
    coronaryArteryDisease: 'yes',
    appetite: 'good',
    hypertension: 'yes',
    diabetes: 'yes',
    anemia: 'yes',
    pedalEdema: 'yes',
  });

  const [responseText, setResponseText] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();

  try {
    const response = await fetch('http://localhost:80/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add any other headers as needed
      },
      body: JSON.stringify(formData),
    });

    if (response.ok) {
      const textResponse = await response.text();
      setResponseText(textResponse); // Set response text in state
    } else {
      throw new Error('Request failed');
    }
  } catch (error) {
    console.error('Error:', error);
  }
};


  return (
  <div>
  <form onSubmit={handleSubmit}>
    <div>
      <label>
        Age:
        <input type="number" name="age" value={formData.age} onChange={handleChange} />
      </label>
    </div>
    <div>
      <label>
        Blood Pressure (mm/HG):
        <input
          type="number"
          name="bloodPressure"
          value={formData.bloodPressure}
          onChange={handleChange}
        />
      </label>
    </div>
    <div>
      <label>
        Red Blood Cell Count:
        <input
          type="number"
          name="redBloodCellCount"
          value={formData.redBloodCellCount}
          onChange={handleChange}
        />
      </label>
    </div>
    <div>
      <label>
        White Blood Cell Count:
        <input
          type="number"
          name="whiteBloodCellCount"
          value={formData.whiteBloodCellCount}
          onChange={handleChange}
        />
      </label>
    </div>
    <div>
      <label>
        Packed Cell Volume:
        <input
          type="number"
          name="packedCellVolume"
          value={formData.packedCellVolume}
          onChange={handleChange}
        />
      </label>
    </div>
    <div>
      <label>
        Serum Creatinine:
        <input
          type="number"
          name="serumCreatinine"
          value={formData.serumCreatinine}
          onChange={handleChange}
        />
      </label>
    </div>
    <div>
      <label>
        Sodium:
        <input
          type="number"
          name="sodium"
          value={formData.sodium}
          onChange={handleChange}
        />
      </label>
    </div>
    <div>
      <label>
        Potassium:
        <input
          type="number"
          name="potassium"
          value={formData.potassium}
          onChange={handleChange}
        />
      </label>
    </div>
    <div>
      <label>
        Hemoglobin:
        <input
          type="number"
          name="hemoglobin"
          value={formData.hemoglobin}
          onChange={handleChange}
        />
      </label>
    </div>
    <div>
      <label>
        Red Blood Cells:
        <select name="redBloodCells" value={formData.redBloodCells} onChange={handleChange}>
          <option value="normal">Normal</option>
          <option value="abnormal">Abnormal</option>
        </select>
      </label>
    </div>
    <div>
      <label>
        Coronary Artery Disease:
        <select
          name="coronaryArteryDisease"
          value={formData.coronaryArteryDisease}
          onChange={handleChange}
        >
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
    </div>
    <div>
      <label>
        Appetite:
        <select name="appetite" value={formData.appetite} onChange={handleChange}>
          <option value="good">Good</option>
          <option value="poor">Poor</option>
        </select>
      </label>
    </div>
    <div>
      <label>
        Hypertension:
        <select name="hypertension" value={formData.hypertension} onChange={handleChange}>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
    </div>
    <div>
      <label>
        Diabetes:
        <select name="diabetes" value={formData.diabetes} onChange={handleChange}>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
    </div>
    <div>
      <label>
        Anemia:
        <select name="anemia" value={formData.anemia} onChange={handleChange}>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
    </div>
    <div>
      <label>
        Pedal Edema:
        <select name="pedalEdema" value={formData.pedalEdema} onChange={handleChange}>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
    </div>
    <button type="submit">Submit</button>
  </form>
  {responseText && (
        <div>
          <h2>Response:</h2>
          <p>{responseText}</p>
        </div>
      )}
  </div>
);
};

export default MyForm;
